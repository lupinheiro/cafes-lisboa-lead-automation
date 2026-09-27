from abc import ABC, abstractmethod


class LeadSource(ABC):
    """Interface para qualquer fonte de leads.

    Permite trocar o Google Places por outra fonte (ex. OpenStreetMap /
    Overpass) sem alterar o resto do pipeline de prospeção.
    """

    @abstractmethod
    async def search(self, region: str, business_types: list[str]) -> list[dict]:
        """Devolve uma lista de negócios encontrados, como dicts brutos."""
        raise NotImplementedError
