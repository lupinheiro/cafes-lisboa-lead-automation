from anthropic import AsyncAnthropic

SYSTEM_PROMPT = (
    "Escreves rascunhos de email de outreach B2B curtos e profissionais em "
    "português europeu, em nome da Cafés Lisboa, para apresentar café em "
    "grão a pastelarias, cafés, bares e restaurantes. Tom direto, sem "
    "exagerar promessas, sem emojis. Termina sempre com uma frase de "
    "opt-out clara (ex.: 'Se preferir não receber mais contactos, basta "
    "responder a dizer.')."
)


class EmailGenerator:
    """Gera rascunhos de email personalizados por lead. Os rascunhos ficam
    sempre pendentes de revisão humana antes de serem enviados."""

    def __init__(self, api_key: str) -> None:
        self._client = AsyncAnthropic(api_key=api_key)

    async def draft_outreach_email(
        self, lead_name: str, business_type: str, address: str | None
    ) -> str:
        location_hint = f" em {address}" if address else ""
        message = await self._client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=400,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Escreve um rascunho de email para {lead_name}, "
                        f"um(a) {business_type}{location_hint}."
                    ),
                }
            ],
        )
        return "".join(block.text for block in message.content if block.type == "text")
