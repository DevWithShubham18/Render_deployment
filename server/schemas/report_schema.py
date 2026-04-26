from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel, Field


class Dataset(BaseModel):
    label: str
    data: List[float]

    backgroundColor: Optional[Union[str, List[str]]] = Field(
        default="rgba(75,192,192,0.5)"
    )
    borderColor: Optional[Union[str, List[str]]] = Field(default="rgba(75,192,192,1)")
    borderWidth: Optional[int] = 1


class ChartData(BaseModel):
    labels: List[str]
    datasets: List[Dataset]


class ChartOptions(BaseModel):
    responsive: Optional[bool] = True
    maintainAspectRatio: Optional[bool] = False
    plugins: Optional[dict] = {}


class ChartConfig(BaseModel):
    type: Literal["bar", "line", "pie", "doughnut"]
    data: ChartData
    options: Optional[ChartOptions] = ChartOptions()


class MultiChartConfig(BaseModel):
    charts: List[ChartConfig]
