from typing import Any, List, Dict
from 


class FileParser:      
    def parse(self, file_path: str) -> str:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if line.startswith("nb_drones:"):
                    data["nb_drones"] = int(line.split(":")[1].strip())

                elif line.startswith("start_hub:"):
                    data["start_hub"] = line.split(":")[1].strip()

                elif line.startswith("hub:"):
                    data["hubs"].append(line.split(":")[1].strip())

                elif line.startswith("end_hub:"):
                    data["end_hub"] = line.split(":")[1].strip()

                elif line.startswith("connection:"):
                    data["connections"].append(line.split(":")[1].strip())
