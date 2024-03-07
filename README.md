#NVIDIA Collector Extension for AppDynamics Machine Agent

###This is an AppDynamics Machine Agent monitor (extension) to gather GPU metrics used in AI (or other) workloads. Metrics are gathered every minute and published to the AppDynamics Metric Browser. The following metrics will be captured:
- Fan Speed
- GPU Temperature
- Power Draw
- Graphics Clock (Mhz)
- Max Graphics Clock (Mhz)
- Mem Clock
- Max Mem Clock (Mhz)
- Sm Clock
- Max Sm Clock (Mhz)
- Video Clock
- Max Video Clock (Mhz)
- Mem Free
- Mem Reserved
- Mem Total
- Mem Used
- Per-Process Memory Usage

##Requirements:
nvidia-smi (provided by NVIDIA Drivers)

##Installation:
```
git clone this repo
mv nvidia-collector /path/to/machine/agent/monitors
sudo systemctl restart appdynamics-machine-agent
```

##Example metrics screenshots below:
<img width="1925" alt="Screenshot 2024-03-07 at 3 05 04 PM" src="https://github.com/kennygarreau/nvidia-collector/assets/99059266/959be819-f6cf-4cba-9f5a-5acb1a68363f">
<img width="1274" alt="Screenshot 2024-03-07 at 3 06 18 PM" src="https://github.com/kennygarreau/nvidia-collector/assets/99059266/296991bc-1bbb-4012-9f61-8dbc940bb879">
