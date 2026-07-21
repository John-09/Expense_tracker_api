from pydantic import BaseModel, ConfigDict, Field, field_validator


class CategoryCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
        examples=["Food"],
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned_name = value.strip()

        if not cleaned_name:
            raise ValueError("Category name cannot be empty")

        return cleaned_name


class CategoryUpdate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
        examples=["Groceries"],
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned_name = value.strip()

        if not cleaned_name:
            raise ValueError("Category name cannot be empty")

        return cleaned_name


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str