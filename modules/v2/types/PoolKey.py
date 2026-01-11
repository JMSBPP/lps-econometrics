from UniswapClient import Client

@dataclass
class PoolKey:
    token0: str 
    token1: str
    lpToken: str

def poolKey(client:Client,token0: str, token1: str) -> PoolKey:
    data = client(
        """
        query GetPair($token0: String!, $token1: String!) {
            pairs(
                where: {
                    or: [
                        {token0: $token0, token1: $token1},
                        {token0: $token1, token1: $token0}
                    ]
                }
                first: 1
            ) {
                id
            }
        }
        """
    )









