import json
import os
from typing import Dict, Any, List, Tuple, Optional

class Data:

    def get(
        self,
        name: str,
    ) -> List[Dict[str, Any]]:
        try:
            path = os.path.join(os.path.dirname(__file__), f'{name}.json')
            if not os.path.exists(path):
                return []
            
            f = open(path)
            return json.load(f)
        except Exception as e:
            print(str(e))
            return []

    def create(
        self,
        name: str,
        data: List[Dict[str, Any]],
    ) -> Tuple[bool, Optional[str]]:
        try:
            path = os.path.join(os.path.dirname(__file__), f'{name}.json')
            if not os.path.exists(path):
                # create the path
                os.mkdir(path)
            with open(path, 'w') as f:
                json.dump(data, f, indent=4)
            
            return True, None
        except Exception as e:
            print(str(e))
            return False, str(e)

    def append(
        self,
        name: str,
        data: Dict[str, Any],
    ) -> Tuple[bool, Optional[str]]:
        try:
            path = os.path.join(os.path.dirname(__file__), f'{name}.json')
            if not os.path.exists(path):
                return False

            ldata = self.get(name)
            ldata.append(data)
            with open(path, 'w') as f:
                json.dump(ldata, f, indent=4)
            
            return True, None
        except Exception as e:
            print(str(e))
            return False, str(e)