/**
 * ============================================================================
 * ElevateRCA — Smart Elevator Live Simulation Module
 * ============================================================================
 * 
 * Modular, real-time physical simulation of a KONE MonoSpace / MiniSpace elevator
 * with EcoDisc PMSM motor, 5-floor hoistway (Ground, 1, 2, 3, 4), dual-sliding doors,
 * counterweight kinematics, continuous software-based Virtual Optical Floor Sensors,
 * dynamic kinematic replay of all telemetry faults (door jam, IGBT trip, rail friction),
 * 10 Live Synthetic Telemetry Sensor Parameter Cards, and strict Technician RTS clearance.
 */

class VirtualFloorSensorArray {
  constructor(floorCount = 5, floorHeights = [0, 25, 50, 75, 100]) {
    this.floorCount = floorCount;
    this.floorHeights = floorHeights; // Ground=0%, 1F=25%, 2F=50%, 3F=75%, 4F=100%
    this.detectionThreshold = 3.2;    // ±3.2% height optical beam capture window
    this.activeFloorIndex = 0;
    this.lastTriggeredFloor = 0;
    this.isBeamBroken = true;
    this.sensorHealth = "ACTIVE";
    this.listeners = [];
  }

  onSensorEvent(callback) {
    this.listeners.push(callback);
  }

  notify(event) {
    this.listeners.forEach(cb => {
      try { cb(event); } catch (e) { console.error("Sensor listener error:", e); }
    });
  }

  update(currentPositionPercent, direction) {
    let triggeredIndex = -1;
    let minDistance = Infinity;

    for (let i = 0; i < this.floorCount; i++) {
      const floorY = this.floorHeights[i];
      const dist = Math.abs(currentPositionPercent - floorY);
      if (dist <= this.detectionThreshold && dist < minDistance) {
        minDistance = dist;
        triggeredIndex = i;
      }
    }

    if (triggeredIndex !== -1) {
      if (!this.isBeamBroken || this.activeFloorIndex !== triggeredIndex) {
        this.isBeamBroken = true;
        this.activeFloorIndex = triggeredIndex;
        this.lastTriggeredFloor = triggeredIndex;
        this.notify({
          type: 'BEAM_TRIGGERED',
          floor: triggeredIndex,
          floorName: triggeredIndex === 0 ? 'Ground (G)' : `Floor ${triggeredIndex}`,
          position: currentPositionPercent,
          deviation: (currentPositionPercent - this.floorHeights[triggeredIndex]).toFixed(2),
          direction: direction,
          timestamp: new Date().toISOString().substring(11, 23)
        });
      }
    } else {
      if (this.isBeamBroken) {
        this.isBeamBroken = false;
        this.notify({
          type: 'BEAM_CLEARED',
          floor: this.activeFloorIndex,
          position: currentPositionPercent,
          direction: direction,
          timestamp: new Date().toISOString().substring(11, 23)
        });
      }
    }

    return {
      activeFloorIndex: this.activeFloorIndex,
      isBeamBroken: this.isBeamBroken,
      detectedFloorName: this.activeFloorIndex === 0 ? 'Ground' : `${this.activeFloorIndex}`
    };
  }

  reset() {
    this.activeFloorIndex = 0;
    this.lastTriggeredFloor = 0;
    this.isBeamBroken = true;
    this.sensorHealth = "ACTIVE";
  }
}


class ElevatorPhysicsEngine {
  constructor(floorHeights = [0, 25, 50, 75, 100]) {
    this.floorHeights = floorHeights;
    this.currentY = 0.0;          // 0.0 = Ground, 100.0 = Floor 4
    this.targetY = 0.0;
    this.targetFloor = 0;
    this.speedPercentPerSec = 22.0; // Responsive kinematic speed (~4.5s for 4 floors)
    this.isMoving = false;
    this.direction = 'IDLE';      // 'UP', 'DOWN', 'IDLE'
    this.isEmergencyStopped = false;
    this.lastTimestamp = null;
    this.onPositionChange = null;
    this.onArrival = null;
    this.animationFrameId = null;
  }

  start() {
    if (this.animationFrameId) return;
    this.lastTimestamp = performance.now();
    this.loop = this.loop.bind(this);
    this.animationFrameId = requestAnimationFrame(this.loop);
  }

  stop() {
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
  }

  moveToFloor(floorIndex) {
    if (this.isEmergencyStopped) return false;
    if (floorIndex < 0 || floorIndex >= this.floorHeights.length) return false;

    this.targetFloor = floorIndex;
    this.targetY = this.floorHeights[floorIndex];

    if (Math.abs(this.currentY - this.targetY) < 0.1) {
      this.currentY = this.targetY;
      this.isMoving = false;
      this.direction = 'IDLE';
      if (this.onArrival) this.onArrival(this.targetFloor);
      return true;
    }

    this.isMoving = true;
    this.direction = this.targetY > this.currentY ? 'UP' : 'DOWN';
    return true;
  }

  emergencyStop() {
    this.isEmergencyStopped = true;
    this.isMoving = false;
    this.direction = 'IDLE';
  }

  resume() {
    this.isEmergencyStopped = false;
  }

  reset() {
    this.isEmergencyStopped = false;
    this.isMoving = false;
    this.direction = 'IDLE';
    this.currentY = 0.0;
    this.targetY = 0.0;
    this.targetFloor = 0;
  }

  loop(timestamp) {
    if (!this.lastTimestamp) this.lastTimestamp = timestamp;
    const rawDt = (timestamp - this.lastTimestamp) / 1000.0;
    const dt = Math.min(Math.max(rawDt, 0.001), 0.05); // Safe dt clamping
    this.lastTimestamp = timestamp;

    if (this.isMoving && !this.isEmergencyStopped) {
      const step = this.speedPercentPerSec * dt;
      const diff = this.targetY - this.currentY;

      if (Math.abs(diff) <= step) {
        this.currentY = this.targetY;
        this.isMoving = false;
        this.direction = 'IDLE';
        if (this.onPositionChange) this.onPositionChange(this.currentY, this.direction);
        if (this.onArrival) this.onArrival(this.targetFloor);
      } else {
        this.currentY += Math.sign(diff) * step;
        if (this.onPositionChange) this.onPositionChange(this.currentY, this.direction);
      }
    }

    this.animationFrameId = requestAnimationFrame(this.loop);
  }
}


class SmartElevatorController {
  constructor() {
    this.floors = [
      { id: 0, label: 'G', name: 'Ground Floor', height: 0 },
      { id: 1, label: '1', name: 'Floor 1', height: 25 },
      { id: 2, label: '2', name: 'Floor 2', height: 50 },
      { id: 3, label: '3', name: 'Floor 3', height: 75 },
      { id: 4, label: '4', name: 'Floor 4', height: 100 }
    ];

    this.currentFloor = 0;
    this.destinationFloor = null;
    this.doorState = 'CLOSED'; // 'CLOSED', 'OPENING', 'OPEN', 'CLOSING', 'JAMMED'
    this.doorPositionPercent = 0; // 0% closed, 100% open
    this.operationalStatus = 'READY'; // 'READY', 'MOVING', 'LEVELING', 'DOOR_OPEN', 'EMERGENCY_STOP', 'FAULT_SIMULATION'
    this.doorTimer = null;
    this.faultAnimTimers = [];
    this.eventLogs = [];
    this.isDoorTransitioning = false;

    // 10 Synthetic Telemetry Sensor Model (Exact mapping to user specification)
    this.telemetry = {
      doorPosition: 0,           // % (0% Closed • 100% Open)
      doorSpeed: 0.00,           // m/s (Normal: 0.35 - 0.50 m/s)
      motorCurrent: 0.3,         // A (Normal: 1.5 - 2.5 A during door move, 0.3A idle)
      openingTime: 1.9,          // s (Normal: 1.5 - 2.2 s)
      closingTime: 1.9,          // s (Normal: 1.5 - 2.3 s)
      vibration: 0.8,            // mm/s (Normal: 0.5 - 1.5 mm/s)
      photoEyeStatus: 'CLEAR',   // 'CLEAR' / 'BLOCKED' (IR Light Beam Safety)
      reopenCount: 0,            // count (Safety Trigger Events)
      motorTemperature: 42.0,    // °C (Normal: 35 - 55 °C)
      doorCycleCount: 1435,      // Total Lifetime Cycles
      isFaultInjected: false,
      activeFaultName: null
    };

    // Instantiate Subsystems
    this.sensors = new VirtualFloorSensorArray(5, [0, 25, 50, 75, 100]);
    this.physics = new ElevatorPhysicsEngine([0, 25, 50, 75, 100]);

    this.telemetryIntervalId = null;
    this.init();
  }

  init() {
    this.sensors.onSensorEvent(event => this.handleSensorEvent(event));

    this.physics.onPositionChange = (currentY, direction) => {
      this.handlePositionUpdate(currentY, direction);
    };

    this.physics.onArrival = (arrivedFloor) => {
      this.handleArrival(arrivedFloor);
    };

    this.physics.start();
    this.logEvent('SYSTEM', 'Smart Elevator Live Simulation Engine initialized. Safety loop healthy.');
    
    // Initial DOM update
    this.renderShaftVisuals(0.0, { activeFloorIndex: 0, isBeamBroken: true });
    this.renderStatusCards();
    this.render10TelemetryCards();
    this.highlightActiveFloorBtn(0);

    // Live 1s synthetic telemetry sensor polling loop
    if (this.telemetryIntervalId) clearInterval(this.telemetryIntervalId);
    this.telemetryIntervalId = setInterval(() => {
      this.updateLiveTelemetryTick();
    }, 1000);
  }

  updateLiveTelemetryTick() {
    if (this.telemetry.isFaultInjected) {
      // Keep fault state active with subtle realistic jitter
      this.render10TelemetryCards();
      return;
    }

    // Realistic normal operating micro-fluctuations
    if (this.physics.isMoving) {
      this.telemetry.motorCurrent = parseFloat((12.5 + (Math.random() * 2.2 - 1.1)).toFixed(1));
      this.telemetry.vibration = parseFloat((0.9 + (Math.random() * 0.3 - 0.15)).toFixed(1));
      this.telemetry.doorSpeed = 0.00;
      this.telemetry.motorTemperature = parseFloat((42.0 + (Math.random() * 0.6)).toFixed(1));
    } else if (this.isDoorTransitioning) {
      this.telemetry.motorCurrent = parseFloat((2.0 + (Math.random() * 0.3 - 0.15)).toFixed(1));
      this.telemetry.doorSpeed = parseFloat((0.40 + (Math.random() * 0.04 - 0.02)).toFixed(2));
      this.telemetry.vibration = parseFloat((0.7 + (Math.random() * 0.2)).toFixed(1));
    } else {
      // Idle at floor
      this.telemetry.motorCurrent = parseFloat((0.3 + (Math.random() * 0.1)).toFixed(1));
      this.telemetry.doorSpeed = 0.00;
      this.telemetry.vibration = parseFloat((0.8 + (Math.random() * 0.1 - 0.05)).toFixed(1));
      this.telemetry.motorTemperature = parseFloat((42.0 + (Math.random() * 0.4 - 0.2)).toFixed(1));
    }

    this.render10TelemetryCards();
  }

  render10TelemetryCards() {
    // 1. Door Position
    const posEl = document.getElementById('simDoorPosVal');
    const posBadge = document.getElementById('simDoorPosBadge');
    if (posEl) posEl.innerText = `${Math.round(this.telemetry.doorPosition)}%`;
    if (posBadge) {
      if (this.telemetry.isFaultInjected && this.doorState === 'JAMMED') {
        posBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-700 border border-amber-300 animate-pulse';
        posBadge.innerText = 'JAMMED (62%)';
      } else {
        posBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200';
        posBadge.innerText = 'OK';
      }
    }

    // 2. Door Speed
    const speedEl = document.getElementById('simDoorSpeedVal');
    const speedBadge = document.getElementById('simDoorSpeedBadge');
    if (speedEl) speedEl.innerText = `${this.telemetry.doorSpeed.toFixed(2)} m/s`;
    if (speedBadge) {
      if (this.telemetry.isFaultInjected && this.telemetry.doorSpeed < 0.15 && this.doorState === 'JAMMED') {
        speedBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-rose-50 text-rose-700 border border-rose-300 font-bold';
        speedBadge.innerText = 'BLOCKED (0.00)';
      } else {
        speedBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200';
        speedBadge.innerText = 'OK';
      }
    }

    // 3. Motor Current
    const currEl = document.getElementById('simMotorCurrVal');
    const currBadge = document.getElementById('simMotorCurrBadge');
    if (currEl) currEl.innerText = `${this.telemetry.motorCurrent.toFixed(1)} A`;
    if (currBadge) {
      if (this.telemetry.motorCurrent > 3.0) {
        currBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-rose-50 text-rose-700 border border-rose-300 font-black animate-pulse';
        currBadge.innerText = 'HIGH SPIKE';
      } else {
        currBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200';
        currBadge.innerText = 'OK';
      }
    }

    // 4. Opening Time
    const openTimeEl = document.getElementById('simOpenTimeVal');
    const openTimeBadge = document.getElementById('simOpenTimeBadge');
    if (openTimeEl) openTimeEl.innerText = `${this.telemetry.openingTime.toFixed(1)} s`;
    if (openTimeBadge) {
      openTimeBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200';
      openTimeBadge.innerText = 'OK';
    }

    // 5. Closing Time
    const closeTimeEl = document.getElementById('simCloseTimeVal');
    const closeTimeBadge = document.getElementById('simCloseTimeBadge');
    if (closeTimeEl) closeTimeEl.innerText = `${this.telemetry.closingTime.toFixed(1)} s`;
    if (closeTimeBadge) {
      if (this.telemetry.closingTime > 3.5) {
        closeTimeBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-rose-50 text-rose-700 border border-rose-300 font-black';
        closeTimeBadge.innerText = 'TIMEOUT';
      } else {
        closeTimeBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200';
        closeTimeBadge.innerText = 'OK';
      }
    }

    // 6. Vibration
    const vibEl = document.getElementById('simVibVal');
    const vibBadge = document.getElementById('simVibBadge');
    if (vibEl) vibEl.innerText = `${this.telemetry.vibration.toFixed(1)} mm/s`;
    if (vibBadge) {
      if (this.telemetry.vibration > 2.0) {
        vibBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-rose-50 text-rose-700 border border-rose-300 font-black animate-pulse';
        vibBadge.innerText = 'ELEVATED';
      } else {
        vibBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200';
        vibBadge.innerText = 'OK';
      }
    }

    // 7. Photo-eye Status
    const peEl = document.getElementById('simPhotoEyeVal');
    const peBadge = document.getElementById('simPhotoEyeBadge');
    if (peEl) peEl.innerText = this.telemetry.photoEyeStatus;
    if (peBadge) {
      if (this.telemetry.photoEyeStatus === 'BLOCKED') {
        peBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-rose-50 text-rose-700 border border-rose-300 font-black';
        peBadge.innerText = 'TRIPPED';
      } else {
        peBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200';
        peBadge.innerText = 'OK';
      }
    }

    // 8. Reopen Count
    const reopenEl = document.getElementById('simReopenVal');
    const reopenBadge = document.getElementById('simReopenBadge');
    if (reopenEl) reopenEl.innerText = `${this.telemetry.reopenCount}`;
    if (reopenBadge) {
      if (this.telemetry.reopenCount >= 3) {
        reopenBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-700 border border-amber-300 font-bold';
        reopenBadge.innerText = 'EXCESSIVE';
      } else {
        reopenBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200';
        reopenBadge.innerText = 'OK';
      }
    }

    // 9. Motor Temperature
    const tempEl = document.getElementById('simMotorTempVal');
    const tempBadge = document.getElementById('simMotorTempBadge');
    if (tempEl) tempEl.innerText = `${this.telemetry.motorTemperature.toFixed(1)} °C`;
    if (tempBadge) {
      if (this.telemetry.motorTemperature > 55.0) {
        tempBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-rose-50 text-rose-700 border border-rose-300 font-black animate-pulse';
        tempBadge.innerText = 'OVERTEMP';
      } else {
        tempBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200';
        tempBadge.innerText = 'OK';
      }
    }

    // 10. Door Cycle Count
    const cycleEl = document.getElementById('simCycleCountVal');
    const cycleBadge = document.getElementById('simCycleCountBadge');
    if (cycleEl) cycleEl.innerText = this.telemetry.doorCycleCount.toLocaleString();
    if (cycleBadge) {
      cycleBadge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200';
      cycleBadge.innerText = 'OK';
    }
  }

  handlePositionUpdate(currentY, direction) {
    const sensorState = this.sensors.update(currentY, direction);
    this.currentFloor = sensorState.activeFloorIndex;

    if (this.physics.isMoving) {
      this.operationalStatus = 'MOVING';
    }

    this.renderShaftVisuals(currentY, sensorState);
    this.renderStatusCards();
  }

  handleSensorEvent(event) {
    if (event.type === 'BEAM_TRIGGERED') {
      this.logEvent('SENSOR', `Optical Beam at ${event.floorName} TRIGGERED (Position: ${event.position.toFixed(1)}%, Dev: ${event.deviation}%)`);
      this.pulseSensorLed(event.floor);
    } else if (event.type === 'BEAM_CLEARED') {
      this.logEvent('SENSOR', `Optical Beam at Floor ${event.floor} CLEARED (Transiting ${event.direction})`);
    }
  }

  handleArrival(floorIndex) {
    this.currentFloor = floorIndex;
    this.destinationFloor = null;
    this.operationalStatus = 'LEVELING';
    this.highlightActiveFloorBtn(floorIndex);
    this.logEvent('CONTROLLER', `Arrived & Leveled at ${this.floors[floorIndex].name} (±0.0mm). Initiating door cycle.`);
    this.renderStatusCards();

    // Auto door open sequence on arrival
    setTimeout(() => {
      this.openDoors(true);
    }, 400);
  }

  callFloor(floorIndex) {
    if (this.physics.isEmergencyStopped) {
      alert('Elevator is in EMERGENCY STOP mode. Click "Reset Normal" or "Resume Operation" first.');
      return;
    }

    if (this.doorState !== 'CLOSED') {
      this.closeDoors(() => {
        this.executeMove(floorIndex);
      });
      return;
    }

    this.executeMove(floorIndex);
  }

  executeMove(floorIndex) {
    if (this.currentFloor === floorIndex && !this.physics.isMoving) {
      this.logEvent('CONTROLLER', `Already at ${this.floors[floorIndex].name}. Opening doors.`);
      this.openDoors(true);
      return;
    }

    this.destinationFloor = floorIndex;
    const dir = floorIndex > this.currentFloor ? 'UP' : 'DOWN';
    this.operationalStatus = 'MOVING';
    this.logEvent('DISPATCH', `Call registered for ${this.floors[floorIndex].name}. Accelerating ${dir}.`);
    
    this.highlightActiveFloorBtn(floorIndex);
    this.physics.moveToFloor(floorIndex);
    this.renderStatusCards();
  }

  openDoors(autoClose = false) {
    if (this.physics.isMoving) {
      this.logEvent('SAFETY', 'Door open command rejected: Elevator in motion.');
      return;
    }
    if (this.physics.isEmergencyStopped) {
      this.logEvent('SAFETY', 'Door open command rejected: Emergency stop engaged.');
      return;
    }

    clearTimeout(this.doorTimer);
    this.clearFaultAnimTimers();
    this.isDoorTransitioning = true;
    this.doorState = 'OPENING';
    this.doorPositionPercent = 50;
    this.telemetry.doorPosition = 50;
    this.telemetry.doorSpeed = 0.40;
    this.telemetry.motorCurrent = 2.0;
    this.operationalStatus = 'DOOR_OPEN';
    this.logEvent('DOOR', `Sliding doors OPENING at ${this.floors[this.currentFloor].name}.`);
    this.renderDoorVisuals();
    this.renderStatusCards();
    this.render10TelemetryCards();

    setTimeout(() => {
      this.doorState = 'OPEN';
      this.doorPositionPercent = 100;
      this.telemetry.doorPosition = 100;
      this.telemetry.doorSpeed = 0.00;
      this.telemetry.motorCurrent = 0.3;
      this.isDoorTransitioning = false;
      this.logEvent('DOOR', `Doors fully OPEN (100%). Passenger exchange.`);
      this.renderDoorVisuals();
      this.renderStatusCards();
      this.render10TelemetryCards();

      if (autoClose) {
        this.doorTimer = setTimeout(() => {
          this.closeDoors();
        }, 1800);
      }
    }, 500);
  }

  closeDoors(callback = null) {
    if (this.doorState === 'CLOSED') {
      if (callback) callback();
      return;
    }

    clearTimeout(this.doorTimer);
    this.clearFaultAnimTimers();
    this.isDoorTransitioning = true;
    this.doorState = 'CLOSING';
    this.doorPositionPercent = 50;
    this.telemetry.doorPosition = 50;
    this.telemetry.doorSpeed = 0.40;
    this.telemetry.motorCurrent = 2.0;
    this.logEvent('DOOR', `Door warning chime: Sliding doors CLOSING.`);
    this.renderDoorVisuals();
    this.renderStatusCards();
    this.render10TelemetryCards();

    setTimeout(() => {
      this.doorState = 'CLOSED';
      this.doorPositionPercent = 0;
      this.telemetry.doorPosition = 0;
      this.telemetry.doorSpeed = 0.00;
      this.telemetry.motorCurrent = 0.3;
      this.telemetry.doorCycleCount += 1;
      this.isDoorTransitioning = false;
      this.operationalStatus = this.physics.isMoving ? 'MOVING' : 'READY';
      this.logEvent('DOOR', `Doors fully CLOSED (0%) & interlocks locked.`);
      this.renderDoorVisuals();
      this.renderStatusCards();
      this.render10TelemetryCards();
      if (callback) callback();
    }, 500);
  }

  emergencyStop() {
    clearTimeout(this.doorTimer);
    this.clearFaultAnimTimers();
    this.physics.emergencyStop();
    this.operationalStatus = 'EMERGENCY_STOP';
    this.logEvent('EMERGENCY', `🚨 EMERGENCY STOP ACTIVATED. Mechanical safety brakes clamped at Y=${this.physics.currentY.toFixed(1)}%. Motion locked.`);
    this.renderStatusCards();
    this.renderEmergencyUI(true);
  }

  resume() {
    if (!this.physics.isEmergencyStopped) return;
    this.physics.resume();
    this.operationalStatus = 'READY';
    this.logEvent('SAFETY', 'Safety chain reset by technician. Emergency state cleared. Ready for dispatch.');
    this.renderStatusCards();
    this.renderEmergencyUI(false);
  }

  clearFaultAnimTimers() {
    this.faultAnimTimers.forEach(t => clearTimeout(t));
    this.faultAnimTimers = [];
  }

  /**
   * Replay exact fault from telemetry incident payload with realistic multi-stage dynamic animation
   */
  simulateFaultFromTrace(trace) {
    if (!trace) return;
    clearTimeout(this.doorTimer);
    this.clearFaultAnimTimers();
    
    // Cleanly reset any lingering physical state
    this.physics.resume();
    const leftDoor = document.getElementById('simDoorLeft');
    const rightDoor = document.getElementById('simDoorRight');
    const cabinEl = document.getElementById('simCabin');
    if (leftDoor) leftDoor.classList.remove('door-jam-shake');
    if (rightDoor) rightDoor.classList.remove('door-jam-shake');
    if (cabinEl) cabinEl.classList.remove('door-jam-shake');

    const primaryAlarm = trace.fault_episode?.primary_alarm?.alarm_code || '';
    const subsystem = trace.fault_episode?.primary_alarm?.subsystem || '';
    const rootCause = trace.hypotheses?.[0]?.root_cause || trace.rca_conclusion?.causal_narrative || 'Door Sill Obstruction';

    this.telemetry.isFaultInjected = true;
    this.telemetry.activeFaultName = `${primaryAlarm} — ${rootCause}`;

    this.logEvent('EMERGENCY', `⚡ REPLAYING TELEMETRY FAULT ANIMATION: [${primaryAlarm}] ${rootCause}`);

    const isDoorFault = subsystem.toLowerCase().includes('door') || primaryAlarm.toLowerCase().includes('door') || rootCause.toLowerCase().includes('door') || rootCause.toLowerCase().includes('sill') || rootCause.toLowerCase().includes('track') || rootCause.toLowerCase().includes('curtain');

    if (isDoorFault) {
      // 1. Initial State: Open doors fully at current landing
      this.doorState = 'OPENING';
      this.doorPositionPercent = 100;
      this.telemetry.doorPosition = 100;
      this.telemetry.doorSpeed = 0.40;
      this.telemetry.motorCurrent = 2.0;
      this.operationalStatus = 'DOOR_OPEN';
      this.renderDoorVisuals();
      this.render10TelemetryCards();
      this.logEvent('DOOR', `Doors OPEN (100%) at ${this.floors[this.currentFloor].name}. Initiating close sequence under telemetry load...`);

      // 2. Step 2 (900ms): Door begins closing with slow kinetic drag
      const t1 = setTimeout(() => {
        this.doorState = 'CLOSING';
        this.telemetry.doorSpeed = 0.24; // Sluggish / delayed speed
        this.telemetry.closingTime = 3.4; // Delay in closing
        this.telemetry.motorCurrent = 3.8; // Elevated torque
        this.logEvent('DOOR', `⚠️ Sliding doors encountering kinetic resistance (Speed: 0.24 m/s, Closing time: 3.4s)...`);
        
        if (leftDoor && rightDoor) {
          leftDoor.style.transform = 'translateX(-56%)';
          rightDoor.style.transform = 'translateX(56%)';
        }
        this.render10TelemetryCards();

        // 3. Step 3 (2000ms): Door JAMMED / STRUCK at 62% opening
        const t2 = setTimeout(() => {
          this.doorState = 'JAMMED';
          this.operationalStatus = 'FAULT_SIMULATION';
          this.doorPositionPercent = 62;

          this.telemetry.doorPosition = 62.0;
          this.telemetry.doorSpeed = 0.00;
          this.telemetry.motorCurrent = 5.8; // High current spike
          this.telemetry.closingTime = 4.8; // Timeout threshold exceeded
          this.telemetry.openingTime = 2.1;
          this.telemetry.vibration = 2.4; // Shaking vibration
          this.telemetry.photoEyeStatus = rootCause.toLowerCase().includes('curtain') || rootCause.toLowerCase().includes('obstruction') ? 'BLOCKED' : 'CLEAR';
          this.telemetry.reopenCount = 3;
          this.telemetry.motorTemperature = 58.0;

          // Apply physical jam vibration shake
          if (leftDoor && rightDoor) {
            leftDoor.classList.add('door-jam-shake');
            rightDoor.classList.add('door-jam-shake');
            leftDoor.style.transform = 'translateX(-56%)';
            rightDoor.style.transform = 'translateX(56%)';
          }

          this.logEvent('DOOR', `🚨 DOOR JAMMED AT 62% STROKE: Mechanical resistance peak. Motor current spiked to 5.8A (over-torque limit). Reopen cycles = 3.`);
          this.renderStatusCards();
          this.render10TelemetryCards();
        }, 1100);
        this.faultAnimTimers.push(t2);

      }, 900);
      this.faultAnimTimers.push(t1);

    } else if (subsystem.toLowerCase().includes('hoist') || subsystem.toLowerCase().includes('mechanical') || primaryAlarm.toLowerCase().includes('vibration') || rootCause.toLowerCase().includes('rail') || rootCause.toLowerCase().includes('bearing')) {
      // Mechanical Rail Jam / Bearing Friction Simulation
      this.physics.reset();
      this.physics.moveToFloor(3);
      this.operationalStatus = 'MOVING';
      this.logEvent('DISPATCH', `Elevator accelerating upwards towards Floor 3...`);
      
      const t1 = setTimeout(() => {
        this.telemetry.vibration = 4.8;
        this.telemetry.motorCurrent = 24.5;
        this.telemetry.motorTemperature = 68.0;
        this.operationalStatus = 'FAULT_SIMULATION';
        if (cabinEl) cabinEl.classList.add('door-jam-shake');
        this.emergencyStop();
        this.logEvent('SAFETY', `🚨 MECHANICAL VIBRATION SPIKE (4.8 mm/s): Guide shoe jam on Rail #2. Safety brakes locked.`);
        this.renderStatusCards();
        this.render10TelemetryCards();
      }, 1400);
      this.faultAnimTimers.push(t1);

    } else {
      // Inverter / IGBT Trip Simulation
      this.physics.reset();
      this.physics.moveToFloor(2);
      this.operationalStatus = 'MOVING';
      this.logEvent('DISPATCH', `Car accelerating with EcoDisc PMSM motor drive...`);

      const t1 = setTimeout(() => {
        this.operationalStatus = 'FAULT_SIMULATION';
        this.telemetry.motorTemperature = 76.5;
        this.telemetry.motorCurrent = 28.0; // Overcurrent spike
        this.telemetry.vibration = 1.8;
        if (cabinEl) cabinEl.classList.add('door-jam-shake');
        this.emergencyStop();
        this.logEvent('SAFETY', `🚨 POWER INVERTER TRIP: IGBT Overcurrent (28.0A) & Thermal overload (76.5°C). Motor drive cut.`);
        this.renderStatusCards();
        this.render10TelemetryCards();
      }, 1300);
      this.faultAnimTimers.push(t1);
    }
  }

  /**
   * Run automated return-to-service test simulation sequence
   */
  runReturnToServiceTest(onComplete) {
    this.clearFaultAnimTimers();
    this.logEvent('SYSTEM', '🧪 RETURN-TO-SERVICE TEST INITIATED (ASME A17.1 / KONE MX10 Standard)...');
    this.operationalStatus = 'READY';

    // Remove any door shake classes
    const leftDoor = document.getElementById('simDoorLeft');
    const rightDoor = document.getElementById('simDoorRight');
    const cabinEl = document.getElementById('simCabin');
    if (leftDoor) leftDoor.classList.remove('door-jam-shake');
    if (rightDoor) rightDoor.classList.remove('door-jam-shake');
    if (cabinEl) cabinEl.classList.remove('door-jam-shake');

    // Step 1: Safety loop check
    setTimeout(() => {
      this.logEvent('SAFETY', '✓ Step 1/3: Safety Circuit Loop 24V Continuity verified. Closed.');
      
      // Step 2: Door cycle check
      setTimeout(() => {
        this.logEvent('DOOR', '✓ Step 2/3: Low-Speed Door Cycle Calibration: 0% ➔ 100% ➔ 0% (Nominal 1.9s, Current 1.8A).');
        this.openDoors(false);
        setTimeout(() => {
          this.closeDoors();
        }, 1200);

        // Step 3: Clear all faults and restore baseline
        setTimeout(() => {
          this.telemetry.isFaultInjected = false;
          this.telemetry.activeFaultName = null;
          this.telemetry.doorPosition = 0;
          this.telemetry.doorSpeed = 0.00;
          this.telemetry.motorCurrent = 0.3;
          this.telemetry.openingTime = 1.9;
          this.telemetry.closingTime = 1.9;
          this.telemetry.vibration = 0.8;
          this.telemetry.photoEyeStatus = 'CLEAR';
          this.telemetry.reopenCount = 0;
          this.telemetry.motorTemperature = 42.0;

          this.renderDoorVisuals();
          this.renderStatusCards();
          this.render10TelemetryCards();
          this.logEvent('SYSTEM', '✅ RETURN-TO-SERVICE TEST COMPLETE: 0 Active Faults. Unit cleared for public service.');

          if (onComplete) onComplete();
        }, 2200);

      }, 1000);
    }, 800);
  }

  resetSimulation() {
    clearTimeout(this.doorTimer);
    this.clearFaultAnimTimers();
    this.physics.reset();
    this.sensors.reset();
    this.currentFloor = 0;
    this.destinationFloor = null;
    this.doorState = 'CLOSED';
    this.doorPositionPercent = 0;
    this.operationalStatus = 'READY';
    this.eventLogs = [];

    const leftDoor = document.getElementById('simDoorLeft');
    const rightDoor = document.getElementById('simDoorRight');
    const cabinEl = document.getElementById('simCabin');
    if (leftDoor) leftDoor.classList.remove('door-jam-shake');
    if (rightDoor) rightDoor.classList.remove('door-jam-shake');
    if (cabinEl) cabinEl.classList.remove('door-jam-shake');

    this.telemetry.isFaultInjected = false;
    this.telemetry.activeFaultName = null;
    this.telemetry.doorPosition = 0;
    this.telemetry.doorSpeed = 0.00;
    this.telemetry.motorCurrent = 0.3;
    this.telemetry.openingTime = 1.9;
    this.telemetry.closingTime = 1.9;
    this.telemetry.vibration = 0.8;
    this.telemetry.photoEyeStatus = 'CLEAR';
    this.telemetry.reopenCount = 0;
    this.telemetry.motorTemperature = 42.0;

    this.logEvent('SYSTEM', 'Simulation reset to Ground Floor. Nominal baseline restored.');
    this.renderShaftVisuals(0.0, { activeFloorIndex: 0, isBeamBroken: true });
    this.renderDoorVisuals();
    this.renderStatusCards();
    this.render10TelemetryCards();
    this.renderEmergencyUI(false);
    this.highlightActiveFloorBtn(0);
  }

  logEvent(category, message) {
    const time = new Date().toISOString().substring(11, 23);
    const entry = { time, category, message };
    this.eventLogs.unshift(entry);
    if (this.eventLogs.length > 35) this.eventLogs.pop();
    this.renderEventLogs();
  }

  renderShaftVisuals(currentY, sensorState) {
    const cabinEl = document.getElementById('simCabin');
    const ropeEl = document.getElementById('simHoistRope');
    const counterweightEl = document.getElementById('simCounterweight');
    const cwRopeEl = document.getElementById('simCwRope');
    const sheaveEl = document.getElementById('simEcoDiscSheave');

    // Cabin motion: bottom 3% at Ground to 81% at Floor 4
    const bottomPercent = currentY * 0.78 + 3.0;

    if (cabinEl) {
      cabinEl.style.bottom = `${bottomPercent}%`;
    }

    if (ropeEl) {
      const ropeHeight = 100 - bottomPercent - 8;
      ropeEl.style.height = `${Math.max(4, ropeHeight)}%`;
    }

    if (counterweightEl) {
      const cwBottomPercent = (100 - currentY) * 0.78 + 3.0;
      counterweightEl.style.bottom = `${cwBottomPercent}%`;
    }

    if (cwRopeEl) {
      const cwRopeHeight = 100 - ((100 - currentY) * 0.78 + 3.0) - 8;
      cwRopeEl.style.height = `${Math.max(4, cwRopeHeight)}%`;
    }

    if (sheaveEl && this.physics.isMoving) {
      const deg = (currentY * 18) % 360;
      sheaveEl.style.transform = `rotate(${this.physics.direction === 'UP' ? deg : -deg}deg)`;
    }

    const carDisp = document.getElementById('simCarFloorDisplay');
    const carArrow = document.getElementById('simCarArrow');
    if (carDisp && sensorState) {
      carDisp.innerText = this.floors[sensorState.activeFloorIndex].label;
    }
    if (carArrow) {
      if (this.physics.direction === 'UP') {
        carArrow.innerHTML = '▲';
        carArrow.className = 'text-[9px] font-bold text-emerald-400 animate-pulse';
      } else if (this.physics.direction === 'DOWN') {
        carArrow.innerHTML = '▼';
        carArrow.className = 'text-[9px] font-bold text-amber-400 animate-pulse';
      } else {
        carArrow.innerHTML = '■';
        carArrow.className = 'text-[9px] text-slate-400';
      }
    }
  }

  renderDoorVisuals() {
    const leftDoor = document.getElementById('simDoorLeft');
    const rightDoor = document.getElementById('simDoorRight');
    if (!leftDoor || !rightDoor) return;

    if (this.doorState === 'OPEN') {
      leftDoor.style.transform = 'translateX(-90%)';
      rightDoor.style.transform = 'translateX(90%)';
    } else if (this.doorState === 'OPENING') {
      leftDoor.style.transform = 'translateX(-50%)';
      rightDoor.style.transform = 'translateX(50%)';
    } else if (this.doorState === 'CLOSING') {
      leftDoor.style.transform = 'translateX(-20%)';
      rightDoor.style.transform = 'translateX(20%)';
    } else if (this.doorState === 'JAMMED') {
      leftDoor.style.transform = 'translateX(-56%)';
      rightDoor.style.transform = 'translateX(56%)';
    } else {
      leftDoor.style.transform = 'translateX(0%)';
      rightDoor.style.transform = 'translateX(0%)';
    }
  }

  pulseSensorLed(floorIndex) {
    const beam = document.getElementById(`simSensorBeam_${floorIndex}`);
    const led = document.getElementById(`simSensorLed_${floorIndex}`);
    if (beam) {
      beam.classList.remove('opacity-0');
      beam.classList.add('opacity-100');
      setTimeout(() => {
        beam.classList.remove('opacity-100');
        beam.classList.add('opacity-0');
      }, 450);
    }
    if (led) {
      led.classList.remove('bg-slate-400', 'border-slate-500');
      led.classList.add('bg-emerald-400', 'border-emerald-200', 'scale-125');
      setTimeout(() => {
        led.classList.remove('bg-emerald-400', 'border-emerald-200', 'scale-125');
        led.classList.add('bg-slate-400', 'border-slate-500');
      }, 450);
    }
  }

  renderStatusCards() {
    const curFloorEl = document.getElementById('simStatCurrentFloor');
    const destFloorEl = document.getElementById('simStatDestination');
    const directionEl = document.getElementById('simStatDirection');
    const statusEl = document.getElementById('simStatStatus');
    const sensorEl = document.getElementById('simStatSensor');
    const doorEl = document.getElementById('simStatDoor');
    const yPosEl = document.getElementById('simStatYPos');

    const curLabel = this.floors[this.currentFloor].name;
    const destLabel = this.destinationFloor !== null ? this.floors[this.destinationFloor].name : '— (IDLE)';

    if (curFloorEl) curFloorEl.innerText = curLabel;
    if (destFloorEl) destFloorEl.innerText = destLabel;
    if (yPosEl) yPosEl.innerText = `${this.physics.currentY.toFixed(1)}% Height`;

    if (directionEl) {
      if (this.physics.direction === 'UP') {
        directionEl.innerHTML = '<span class="text-emerald-700 flex items-center space-x-1 font-bold"><i data-lucide="arrow-up" class="w-3.5 h-3.5"></i><span>MOVING UP</span></span>';
      } else if (this.physics.direction === 'DOWN') {
        directionEl.innerHTML = '<span class="text-amber-700 flex items-center space-x-1 font-bold"><i data-lucide="arrow-down" class="w-3.5 h-3.5"></i><span>MOVING DOWN</span></span>';
      } else {
        directionEl.innerHTML = '<span class="text-slate-600 font-bold">IDLE (AT REST)</span>';
      }
    }

    if (statusEl) {
      const colors = {
        READY: 'bg-emerald-50 text-emerald-700 border-emerald-200',
        MOVING: 'bg-kone-50 text-kone-700 border-kone-200',
        LEVELING: 'bg-purple-50 text-purple-700 border-purple-200',
        DOOR_OPEN: 'bg-sky-50 text-sky-700 border-sky-200',
        EMERGENCY_STOP: 'bg-rose-50 text-rose-700 border-rose-200 font-bold',
        FAULT_SIMULATION: 'bg-rose-50 text-rose-700 border-rose-300 font-bold animate-pulse'
      };
      const badge = colors[this.operationalStatus] || 'bg-slate-100 text-slate-700 border-slate-200';
      statusEl.className = `px-2 py-0.5 rounded text-[10px] font-mono font-bold border ${badge}`;
      statusEl.innerText = this.operationalStatus;
    }

    if (sensorEl) {
      if (this.sensors.isBeamBroken) {
        sensorEl.innerHTML = `<span class="text-emerald-700 font-bold font-mono flex items-center space-x-1"><span class="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span><span>BEAM TRIGGERED (${this.floors[this.currentFloor].label})</span></span>`;
      } else {
        sensorEl.innerHTML = '<span class="text-slate-600 font-mono font-medium">BEAM CLEAR (MONITORING)</span>';
      }
    }

    if (doorEl) {
      const dColors = {
        CLOSED: 'text-slate-700',
        OPENING: 'text-amber-600 font-bold',
        OPEN: 'text-emerald-700 font-bold',
        CLOSING: 'text-purple-600 font-bold',
        JAMMED: 'text-rose-700 font-black animate-pulse'
      };
      const color = dColors[this.doorState] || 'text-slate-700';
      doorEl.className = `font-bold text-xs font-mono ${color}`;
      doorEl.innerText = this.doorState;
    }

    if (window.lucide) window.lucide.createIcons();
  }

  highlightActiveFloorBtn(floorIndex) {
    this.floors.forEach(f => {
      const btn = document.getElementById(`simFloorBtn_${f.id}`);
      if (!btn) return;
      if (f.id === floorIndex) {
        btn.classList.remove('bg-white', 'text-slate-700', 'border-slate-300');
        btn.classList.add('bg-kone-500', 'text-white', 'border-kone-600', 'ring-2', 'ring-kone-300', 'font-black');
      } else {
        btn.classList.remove('bg-kone-500', 'text-white', 'border-kone-600', 'ring-2', 'ring-kone-300', 'font-black');
        btn.classList.add('bg-white', 'text-slate-700', 'border-slate-300');
      }
    });
  }

  renderEmergencyUI(isEmergency) {
    const banner = document.getElementById('simEmergencyBanner');
    const stopBtn = document.getElementById('simEmergencyStopBtn');
    const resumeBtn = document.getElementById('simResumeBtn');

    if (banner) banner.classList.toggle('hidden', !isEmergency);
    if (stopBtn) stopBtn.classList.toggle('opacity-50', isEmergency);
    if (resumeBtn) resumeBtn.classList.toggle('opacity-50', !isEmergency);
  }

  renderEventLogs() {
    const listEl = document.getElementById('simEventLogList');
    if (!listEl) return;

    listEl.innerHTML = this.eventLogs.map(log => {
      const colors = {
        SYSTEM: 'text-slate-600 bg-slate-100 border-slate-200',
        SENSOR: 'text-emerald-700 bg-emerald-50 border-emerald-200 font-bold',
        CONTROLLER: 'text-kone-700 bg-kone-50 border-kone-200',
        DISPATCH: 'text-purple-700 bg-purple-50 border-purple-200',
        DOOR: 'text-sky-700 bg-sky-50 border-sky-200',
        SAFETY: 'text-amber-800 bg-amber-50 border-amber-200',
        EMERGENCY: 'text-rose-700 bg-rose-50 border-rose-200 font-bold'
      };
      const badgeStyle = colors[log.category] || colors.SYSTEM;

      return `
        <div class="p-2 rounded-lg bg-white border border-slate-200 flex items-start justify-between text-[11px] font-mono shadow-2xs hover:bg-slate-50 transition">
          <div class="flex items-center space-x-2">
            <span class="px-1.5 py-0.5 rounded text-[9px] uppercase border ${badgeStyle}">${log.category}</span>
            <span class="text-slate-800 font-medium">${log.message}</span>
          </div>
          <span class="text-slate-400 text-[10px] whitespace-nowrap pl-2">${log.time}</span>
        </div>
      `;
    }).join('');
  }
}

// Global Singleton Instance & Window Bindings
window.elevatorSim = null;

function initElevatorSimulation() {
  if (!window.elevatorSim) {
    window.elevatorSim = new SmartElevatorController();
  }
  return window.elevatorSim;
}

// Global Direct Event Dispatchers (fail-safe for inline onclicks)
window.callElevatorFloor = function(floor) {
  const sim = window.elevatorSim || initElevatorSimulation();
  sim.callFloor(floor);
};

window.openElevatorDoors = function() {
  const sim = window.elevatorSim || initElevatorSimulation();
  sim.openDoors();
};

window.closeElevatorDoors = function() {
  const sim = window.elevatorSim || initElevatorSimulation();
  sim.closeDoors();
};

window.emergencyStopElevator = function() {
  const sim = window.elevatorSim || initElevatorSimulation();
  sim.emergencyStop();
};

window.resumeElevator = function() {
  const sim = window.elevatorSim || initElevatorSimulation();
  sim.resume();
};

window.resetElevatorSimulation = function() {
  const sim = window.elevatorSim || initElevatorSimulation();
  sim.resetSimulation();
};

// Auto-initialize when script loads
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => initElevatorSimulation());
} else {
  initElevatorSimulation();
}
