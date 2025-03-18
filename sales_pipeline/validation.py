from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

class AirbnbTransaction(BaseModel):
    Items: str
    Cost: float
    Month: datetime
    Transaction_Type: str
    Total_Income: float
    Total_Expense: float
    Total_Cleaning_for_All_Time: float
    Net_Profit: float

    @validator('Cost')
    def cost_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Cost must be positive')
        return v 