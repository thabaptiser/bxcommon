from typing import Optional, List, Union, Any, Dict, Tuple

from bxcommon.rpc.provider.abstract_ws_provider import AbstractWsProvider
from bxcommon.rpc.bx_json_rpc_request import BxJsonRpcRequest
from bxcommon.rpc.json_rpc_response import JsonRpcResponse
from bxcommon.rpc.rpc_errors import RpcError
from bxcommon.rpc.rpc_request_type import RpcRequestType


class WsClient(AbstractWsProvider):
    async def call_bx(
        self,
        method: RpcRequestType,
        params: Union[List[Any], Dict[Any, Any], None],
        request_id: Optional[str] = None
    ) -> JsonRpcResponse:
        if request_id is None:
            request_id = str(self.current_request_id)
            self.current_request_id += 1

        return await self.call(
            BxJsonRpcRequest(request_id, method, params)
        )

    async def subscribe(self, channel: str, options: Optional[Dict[str, Any]] = None) -> str:
        if options is None:
            options = {}
        response = await self.call_bx(
            RpcRequestType.SUBSCRIBE, [channel, options]
        )
        subscription_id = response.result
        assert isinstance(subscription_id, str)
        self.subscription_manager.register_subscription(subscription_id)
        return subscription_id

    async def unsubscribe(self, subscription_id: str) -> Tuple[bool, Optional[RpcError]]:
        response = await self.call_bx(RpcRequestType.UNSUBSCRIBE, [subscription_id])
        if response.result is not None:
            self.subscription_manager.unregister_subscription(subscription_id)
            return True, None
        else:
            return False, response.error
