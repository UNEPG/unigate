from typing import Tuple, List, Dict, Union, Optional

from pydantic import BaseModel
from datetime import datetime

""" Bme """


class BmeDataBase(BaseModel):
    temperature: float
    pressure: float
    humidity: float


class BmeDataBaseTime(BmeDataBase):
    id: Optional[int]
    updated: datetime


""" Bno """


class BnoDataBase(BaseModel):
    temperature: float
    acceleration: Dict[str, Union[int, float]]
    magnetic: Dict[str, Union[int, float]]
    gyro: Dict[str, Union[int, float]]
    euler: Dict[str, Union[int, float]]
    quaternion: Dict[str, Union[int, float]]
    linear_acceleration: Dict[str, Union[int, float]]
    gravity: Dict[str, Union[int, float]]


class BnoDataBaseTime(BnoDataBase):
    id: Optional[int]
    updated: datetime


""" Si """


class SiDataBase(BaseModel):
    vis: int
    ir: int
    uv: int


class SiDataBaseTime(SiDataBase):
    id: Optional[int]
    updated: datetime


""" Vcmd """


class VcmdSchemaBase(BaseModel):
    updated: datetime
    cam_supported: int
    cam_detected: int
    state: bytes
    temperature: float
    arm_clock: int
    core_clock: int
    serial_clock: int
    storage_clock: int
    voltage: float
    otp: Dict[str, str]
    cpu_memory: int
    gpu_memory: int
    config: Dict[str, Union[str, int]]
    space: Dict[str, int]
    memory: Dict[str, Union[int, float]]


class VcmdSchema(VcmdSchemaBase):
    id: Optional[int]


''' Camera '''


class CameraSchema(BaseModel):
    id: Optional[int]
    updated: datetime
    cam_num: int
    path: str
