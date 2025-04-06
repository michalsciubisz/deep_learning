from typing import Union
from enum import Enum

class RobotSize(Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'

class RobotSizeError(Exception):
    def __init__(self, message="Wrong type of robot size."):
        self.message = message
        super().__init__(self.message)

class Robot:
    def __init__(self, id: str, size: Union[RobotSize, str] = RobotSize.SMALL) -> None:
        if isinstance(size, str):
            size = [matching_size for matching_size in RobotSize if size == matching_size.value][0]

        self.id = id
        self.size = size
        self.load_capacity = self.calculate_capacity()
        self.velocity = self.calculate_velocity()

    def calculate_capacity(self):
        if self.size == RobotSize.SMALL:
            return 2
        elif self.size == RobotSize.MEDIUM:
            return 4
        elif self.size == RobotSize.LARGE:
            return 7
        else:
            raise RobotSizeError
    
    def calculate_velocity(self):
        if self.size == RobotSize.SMALL:
            return 1
        elif self.size == RobotSize.MEDIUM:
            return 0.7
        elif self.size == RobotSize.LARGE:
            return 0.4
        else:
            raise RobotSizeError