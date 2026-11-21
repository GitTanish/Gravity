# Gravity

A Python Newtonian gravity simulation, currently focused on an idealized Earth–Moon system. The project initializes circular orbits around a shared barycenter, advances bodies with velocity Verlet integration, and checks physical invariants through automated tests.

## Current scope

Implemented:

- Three-dimensional body state using NumPy `float64` vectors.
- Earth–Moon initial conditions in the X–Z plane, with the barycenter at the origin.
- Pairwise Newtonian gravitational acceleration for a list of bodies.
- Fixed-timestep velocity Verlet integration.
- Kinetic, gravitational potential, and total energy diagnostics.
- Angular momentum diagnostics.
- Tests for initial conditions and conservation over approximately one orbit.

The physics can run headlessly through the Python API and tests. There is no runnable application or interactive display yet: `main.py` is empty, and the `visualization/`, `input/`, and `field/` directories are placeholders. Display and time-warp constants are defined but are not connected to an application loop.

## Setup

Python 3.11 is the currently verified environment. Run these commands from the project root (`Gravity/`).

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Dependencies:

- **NumPy** — vectors and numerical calculations.
- **pytest** — automated tests.
- **Pygame** — listed as a dependency for visualization; not currently used by the implemented physics.

## Run the tests

With the virtual environment active, run from the project root:

```powershell
python -m pytest tests/
```

To run only the conservation tests:

```powershell
python -m pytest tests/test_conservation.py
```

Use `python -m pytest` from the project root so Python can resolve local modules such as `simulation` and `physics`. Running from inside `tests/` can cause `ModuleNotFoundError`.

The five tests cover:

- The barycenter lying inside Earth.
- An initial orbital period between 27.2 and 27.5 days.
- Near-zero initial total linear momentum, using a scale-aware floating-point tolerance.
- The circular-orbit energy relationship: `K = -U / 2`.
- Final energy and angular momentum relative to their initial values after approximately one orbit, using a 60-second timestep.

The conservation test compares the beginning and end of the run; it does not measure the maximum error throughout the orbit.

## Run a headless simulation

From the project root, start `python` and run:

```python
from simulation.orbital_setup import create_earth_moon_system
from physics.integrators.verlet import compute_acceleration, step_velocity_verlet
from physics.diagnostics import compute_total_energy

earth, moon, stats = create_earth_moon_system()
bodies = [earth, moon]

# Initialize acceleration before taking the first Verlet step.
for body, acceleration in zip(bodies, compute_acceleration(bodies)):
    body.acceleration = acceleration

_, _, initial_energy = compute_total_energy(bodies)

dt = 60.0  # Simulated seconds per step.
steps = int(stats["period_days"] * 86400.0 / dt)
for _ in range(steps):
    step_velocity_verlet(bodies, dt)

_, _, final_energy = compute_total_energy(bodies)
print("Earth position (m):", earth.position)
print("Moon position (m):", moon.position)
print("Relative energy error:", abs(final_energy - initial_energy) / abs(initial_energy))
```

`step_velocity_verlet` updates bodies in place. It requires valid accelerations at the current positions before the first step; newly created bodies initially have zero acceleration. Subsequent steps update acceleration automatically.

## Project layout

```text
Gravity/
├── config/
│   └── constants.py          # Physical constants and future display settings
├── simulation/
│   ├── body.py               # Body state and trail storage
│   └── orbital_setup.py      # Earth–Moon circular-orbit initialization
├── physics/
│   ├── diagnostics.py        # Energy and angular momentum
│   └── integrators/
│       └── verlet.py         # Pairwise acceleration and velocity Verlet
├── tests/
│   ├── test_setup.py         # Initial-condition checks
│   └── test_conservation.py  # Energy and angular-momentum checks
├── field/                    # Placeholder
├── input/                    # Placeholder
├── visualization/            # Placeholder
├── main.py                   # Empty application entry point
└── requirements.txt
```

## Model and limitations

- Physics uses SI units: meters, kilograms, and seconds. Setup statistics explicitly labeled `_km` or `_days` are converted for reporting.
- Initial Earth–Moon motion is circular and isolated, not an ephemeris-based model of the real system. Solar perturbations and other external forces are not included.
- Gravity treats bodies as point masses. Stored radii do not provide collision detection or contact physics.
- Pairwise acceleration has O(N²) computational cost and no gravitational softening. Coincident positions are skipped rather than resolved as collisions; close encounters require particular care with timestep choice.
- Integration is fixed-step, with no adaptive timestep control. Conservation accuracy depends on the system, timestep, and duration.
- Calculations use floating-point arithmetic, so conserved quantities should be checked with appropriate tolerances rather than exact equality.

## Next steps

- Add an application loop that connects initialization, stepping, and diagnostics.
- Implement visualization and user input.
- Extend validation to longer runs, intermediate conservation errors, and additional orbital configurations.
