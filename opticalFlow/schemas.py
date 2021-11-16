from pydantic import BaseModel
from typing import Optional

"""This schemas file is for pydantic schemas for validating requests and configurations for models"""

class BaseRequest(BaseModel):
    customer: str # who sent the request


class OutputVideoParams(BaseModel):
    fps: int


class ShitomasiParams(BaseModel):
    qualityLevel: float
    minDistance: int
    blockSize: int


class LKParams(BaseModel):
    winSize: tuple[int]
    maxLevel: int
    criteria: Optional[tuple] = None # might be not needed or have to be configured in other way


class FarneBackFonfiguration(BaseModel):
    savevid: Optional[bool] = None
    output_video_params: Optional[OutputVideoParams] = None
    pyr_scale: float
    levels: int
    winsize: int
    iterations: int
    poly_n: int
    poly_sigma: int
    #optflow_farneback_gaussian: int # might be configured strait from cv


class FarneBack(BaseRequest):
    configuration_params: Optional[FarneBackFonfiguration] = None


class LucasKanadeConfiguration(BaseModel):
    savevid: Optional[bool] = None
    output_video_params: Optional[OutputVideoParams] = None
    numPts: int
    trailLength: int
    trailThickness: int
    trailFade: int 
    pointSize: int
    shitomasi_params: ShitomasiParams
    lk_params: Optional[LKParams] = None # might be configured other way (model settings as default)


class LucasKanade(BaseRequest):
    configuration: Optional[LucasKanadeConfiguration] = None
