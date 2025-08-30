from pydantic import BaseModel, Field, root_validator
from typing import Optional

class Order(BaseModel):
    product_name: str
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    discount: float = Field(0, ge=0, le=1)
    total_price: Optional[float]
    shipping_required: bool = False
    shipping_cost: float = 0

    @root_validator
    def check_totals_and_shipping(cls, values):
        qty = values.get("quantity")
        price = values.get("unit_price")
        discount = values.get("discount")
        total = values.get("total_price")
        shipping_required = values.get("shipping_required")
        shipping_cost = values.get("shipping_cost")

        expected_total = qty * price * (1 - discount)

        if total is not None and round(total, 2) != round(expected_total, 2):
            raise ValueError(f"El total {total} no coincide con el esperado {expected_total}")

        if shipping_required and shipping_cost <= 0:
            raise ValueError("Debe agregar costo de envío si shipping_required=True")

        return values
