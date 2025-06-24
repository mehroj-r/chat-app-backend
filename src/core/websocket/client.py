class WSClient():
    """Provides higher level abstraction over channel layer operations like sending messages and managing groups."""

    def __init__(self, channel_layer=None) -> None:
        self.channel_layer = channel_layer

    async def add_to_group(self, group: str, channel: str) -> None:
        await self.channel_layer.group_add(group, channel)

    async def remove_from_group(self, group: str, channel: str) -> None:
        await self.channel_layer.group_discard(group, channel)

    async def send_to_group(self, group: str, event: dict) -> None:
        await self.channel_layer.group_send(group, event)