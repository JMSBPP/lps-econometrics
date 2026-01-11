from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, List, Dict, Any
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class Client:
    ENDPOINT = os.getenv("INDEXER")
    def __call__(self, query: str, variables: Optional[Dict[str, Any]] = None)-> Dict[str, Any]:
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        response = requests.post(
            ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        result = response.json()

        if "errors" in result:
            raise Exception(f"GraphQL errors: {result['errors']}")

        return result.get("data", {})


    def get_pair_info(self) -> Optional[PairInfo]:
        """Get current information about the pair."""
        if self._pair_info:
            return self._pair_info

        pair_id = self.get_pair_id()
        if not pair_id:
            return None

        query = """
        query GetPairInfo($pairId: ID!) {
            pair(id: $pairId) {
                id
                token0 { id symbol }
                token1 { id symbol }
                reserve0
                reserve1
                reserveUSD
                liquidityProviderCount
                totalSupply
                createdAtTimestamp
                createdAtBlockNumber
                txCount
                volumeUSD
            }
        }
        """

        data = self._query(query, {"pairId": pair_id})
        pair = data.get("pair")

        if pair:
            self._pair_info = PairInfo(
                id=pair["id"],
                token0_symbol=pair["token0"]["symbol"],
                token1_symbol=pair["token1"]["symbol"],
                token0_address=pair["token0"]["id"],
                token1_address=pair["token1"]["id"],
                reserve0=float(pair["reserve0"]),
                reserve1=float(pair["reserve1"]),
                reserve_usd=float(pair["reserveUSD"]),
                liquidity_provider_count=int(pair["liquidityProviderCount"]),
                total_supply=float(pair["totalSupply"]),
                created_at_timestamp=int(pair["createdAtTimestamp"]),
                created_at_block=int(pair["createdAtBlockNumber"]),
                tx_count=int(pair["txCount"]),
                volume_usd=float(pair["volumeUSD"])
            )
            return self._pair_info

        return None

    def get_pair_hour_data(
        self,
        start_timestamp: Optional[int] = None,
        end_timestamp: Optional[int] = None,
        first: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        Get hourly aggregated data for the pair.

        Args:
            start_timestamp: Unix timestamp to start from (inclusive)
            end_timestamp: Unix timestamp to end at (inclusive)
            first: Maximum number of records to return
        """
        pair_id = self.get_pair_id()
        if not pair_id:
            return []

        where_clause = f'pair: "{pair_id}"'
        if start_timestamp:
            where_clause += f", hourStartUnix_gte: {start_timestamp}"
        if end_timestamp:
            where_clause += f", hourStartUnix_lte: {end_timestamp}"

        query = f"""
        {{
            pairHourDatas(
                where: {{{where_clause}}}
                first: {first}
                orderBy: hourStartUnix
                orderDirection: asc
            ) {{
                id
                hourStartUnix
                reserve0
                reserve1
                totalSupply
                reserveUSD
                hourlyVolumeToken0
                hourlyVolumeToken1
                hourlyVolumeUSD
                hourlyTxns
            }}
        }}
        """

        data = self._query(query)
        return data.get("pairHourDatas", [])

    def get_pair_day_data(
        self,
        start_date: Optional[int] = None,
        end_date: Optional[int] = None,
        first: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        Get daily aggregated data for the pair.

        Args:
            start_date: Unix timestamp (day) to start from
            end_date: Unix timestamp (day) to end at
            first: Maximum number of records to return
        """
        pair_id = self.get_pair_id()
        if not pair_id:
            return []

        pair_address = pair_id  # pair_id is the address
        where_clause = f'pairAddress: "{pair_address}"'
        if start_date:
            where_clause += f", date_gte: {start_date}"
        if end_date:
            where_clause += f", date_lte: {end_date}"

        query = f"""
        {{
            pairDayDatas(
                where: {{{where_clause}}}
                first: {first}
                orderBy: date
                orderDirection: asc
            ) {{
                id
                date
                reserve0
                reserve1
                totalSupply
                reserveUSD
                dailyVolumeToken0
                dailyVolumeToken1
                dailyVolumeUSD
                dailyTxns
            }}
        }}
        """

        data = self._query(query)
        return data.get("pairDayDatas", [])

    def get_mints(
        self,
        start_timestamp: Optional[int] = None,
        end_timestamp: Optional[int] = None,
        first: int = 1000
    ) -> List[Dict[str, Any]]:
        """Get mint (liquidity addition) events for the pair."""
        pair_id = self.get_pair_id()
        if not pair_id:
            return []

        where_clause = f'pair: "{pair_id}"'
        if start_timestamp:
            where_clause += f", timestamp_gte: {start_timestamp}"
        if end_timestamp:
            where_clause += f", timestamp_lte: {end_timestamp}"

        query = f"""
        {{
            mints(
                where: {{{where_clause}}}
                first: {first}
                orderBy: timestamp
                orderDirection: asc
            ) {{
                id
                timestamp
                to
                sender
                liquidity
                amount0
                amount1
                amountUSD
                transaction {{
                    id
                    blockNumber
                }}
            }}
        }}
        """

        data = self._query(query)
        return data.get("mints", [])

    def get_burns(
        self,
        start_timestamp: Optional[int] = None,
        end_timestamp: Optional[int] = None,
        first: int = 1000
    ) -> List[Dict[str, Any]]:
        """Get burn (liquidity removal) events for the pair."""
        pair_id = self.get_pair_id()
        if not pair_id:
            return []

        where_clause = f'pair: "{pair_id}"'
        if start_timestamp:
            where_clause += f", timestamp_gte: {start_timestamp}"
        if end_timestamp:
            where_clause += f", timestamp_lte: {end_timestamp}"

        query = f"""
        {{
            burns(
                where: {{{where_clause}}}
                first: {first}
                orderBy: timestamp
                orderDirection: asc
            ) {{
                id
                timestamp
                sender
                to
                liquidity
                amount0
                amount1
                amountUSD
                transaction {{
                    id
                    blockNumber
                }}
            }}
        }}
        """

        data = self._query(query)
        return data.get("burns", [])

    def count_active_lps_over_time(
        self,
        frequency: Frequency = Frequency.DAY,
        start_timestamp: Optional[int] = None,
        end_timestamp: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Calculate the number of active LPs over time by tracking mint/burn events.

        An LP is considered "active" if they have added liquidity and not fully withdrawn.
        This reconstructs historical LP counts from mint/burn events.

        Args:
            frequency: Time bucket size for aggregation
            start_timestamp: Start of time range
            end_timestamp: End of time range

        Returns:
            List of dicts with timestamp and active_lp_count
        """
        # Get all mints and burns
        mints = self.get_mints(start_timestamp, end_timestamp, first=5000)
        burns = self.get_burns(start_timestamp, end_timestamp, first=5000)

        # Track LP balances over time
        lp_balances: Dict[str, float] = {}  # address -> liquidity balance
        events = []

        for mint in mints:
            events.append({
                "timestamp": int(mint["timestamp"]),
                "type": "mint",
                "address": mint["to"],
                "liquidity": float(mint["liquidity"]) if mint["liquidity"] else 0,
                "block": int(mint["transaction"]["blockNumber"])
            })

        for burn in burns:
            events.append({
                "timestamp": int(burn["timestamp"]),
                "type": "burn",
                "address": burn["sender"] or burn["to"],
                "liquidity": float(burn["liquidity"]) if burn["liquidity"] else 0,
                "block": int(burn["transaction"]["blockNumber"])
            })

        # Sort by timestamp
        events.sort(key=lambda x: (x["timestamp"], x["block"]))

        # Calculate active LPs at each point
        results = []
        for event in events:
            addr = event["address"]
            if addr:
                if event["type"] == "mint":
                    lp_balances[addr] = lp_balances.get(addr, 0) + event["liquidity"]
                else:
                    lp_balances[addr] = max(0, lp_balances.get(addr, 0) - event["liquidity"])

            active_lps = sum(1 for bal in lp_balances.values() if bal > 0)
            results.append({
                "timestamp": event["timestamp"],
                "block_number": event["block"],
                "active_lp_count": active_lps,
                "event_type": event["type"]
            })

        # Aggregate by frequency if needed
        if frequency != Frequency.HOUR:
            results = self._aggregate_by_frequency(results, frequency)

        return results

    def _aggregate_by_frequency(
        self,
        data: List[Dict[str, Any]],
        frequency: Frequency
    ) -> List[Dict[str, Any]]:
        """Aggregate data points by the specified frequency, keeping max LP count per period."""
        if not data:
            return []

        # Determine bucket size in seconds
        bucket_sizes = {
            Frequency.HOUR: 3600,
            Frequency.DAY: 86400,
            Frequency.WEEK: 604800,
            Frequency.MONTH: 2592000,  # ~30 days
            Frequency.YEAR: 31536000
        }
        bucket_size = bucket_sizes[frequency]

        # Group by bucket
        buckets: Dict[int, List[Dict[str, Any]]] = {}
        for item in data:
            bucket = (item["timestamp"] // bucket_size) * bucket_size
            if bucket not in buckets:
                buckets[bucket] = []
            buckets[bucket].append(item)

        # Get max LP count per bucket
        results = []
        for bucket_ts, items in sorted(buckets.items()):
            max_item = max(items, key=lambda x: x["active_lp_count"])
            results.append({
                "timestamp": bucket_ts,
                "block_number": max_item["block_number"],
                "active_lp_count": max_item["active_lp_count"],
                "period_start": datetime.utcfromtimestamp(bucket_ts).isoformat()
            })

        return results

    def getTimeData(
        self,
        filter: Filter = Filter.NUMBER_OF_ACTIVE_LPS,
        frequency: Frequency = Frequency.MONTH,
        start_timestamp: Optional[int] = None,
        end_timestamp: Optional[int] = None
    ) -> Optional[TimeData]:
        """
        Find the TimeData for the pool based on the specified filter criteria.

        For NUMBER_OF_ACTIVE_LPS: Returns the TimeData when there was the maximum
        number of liquidity providers with active liquidity on the pool.

        For MAX_LIQUIDITY_USD: Returns the TimeData when the pool had maximum USD liquidity.

        For MAX_VOLUME_USD: Returns the TimeData when the pool had maximum daily volume.

        For MAX_TRANSACTIONS: Returns the TimeData when the pool had most transactions.

        Args:
            filter: The criteria to use for finding the optimal time period
            frequency: Time granularity for analysis (HOUR, DAY, WEEK, MONTH, YEAR)
            start_timestamp: Start of date range (unix timestamp), defaults to pool creation
            end_timestamp: End of date range (unix timestamp), defaults to now

        Returns:
            TimeData object representing the point in time matching the filter criteria,
            or None if no data is available.
        """
        pair_info = self.get_pair_info()
        if not pair_info:
            return None

        # Set default time range
        if start_timestamp is None:
            start_timestamp = pair_info.created_at_timestamp
        if end_timestamp is None:
            end_timestamp = int(datetime.utcnow().timestamp())

        if filter == Filter.NUMBER_OF_ACTIVE_LPS:
            # Track LP activity over time and find maximum
            lp_data = self.count_active_lps_over_time(
                frequency=frequency,
                start_timestamp=start_timestamp,
                end_timestamp=end_timestamp
            )

            if not lp_data:
                return None

            # Find the time with maximum active LPs
            max_point = max(lp_data, key=lambda x: x["active_lp_count"])

            return TimeData(
                block_number=max_point["block_number"],
                block_timestamp=max_point["timestamp"],
                unix_timestamp=max_point["timestamp"]
            )

        elif filter == Filter.MAX_LIQUIDITY_USD:
            # Use daily data to find max liquidity
            if frequency == Frequency.HOUR:
                data = self.get_pair_hour_data(start_timestamp, end_timestamp)
                if not data:
                    return None
                max_point = max(data, key=lambda x: float(x["reserveUSD"]))
                return TimeData(
                    block_number=0,  # Hour data doesn't have block number
                    block_timestamp=int(max_point["hourStartUnix"]),
                    unix_timestamp=int(max_point["hourStartUnix"])
                )
            else:
                data = self.get_pair_day_data(start_timestamp, end_timestamp)
                if not data:
                    return None
                max_point = max(data, key=lambda x: float(x["reserveUSD"]))
                return TimeData(
                    block_number=0,  # Day data doesn't have block number
                    block_timestamp=int(max_point["date"]),
                    unix_timestamp=int(max_point["date"])
                )

        elif filter == Filter.MAX_VOLUME_USD:
            if frequency == Frequency.HOUR:
                data = self.get_pair_hour_data(start_timestamp, end_timestamp)
                if not data:
                    return None
                max_point = max(data, key=lambda x: float(x["hourlyVolumeUSD"]))
                return TimeData(
                    block_number=0,
                    block_timestamp=int(max_point["hourStartUnix"]),
                    unix_timestamp=int(max_point["hourStartUnix"])
                )
            else:
                data = self.get_pair_day_data(start_timestamp, end_timestamp)
                if not data:
                    return None
                max_point = max(data, key=lambda x: float(x["dailyVolumeUSD"]))
                return TimeData(
                    block_number=0,
                    block_timestamp=int(max_point["date"]),
                    unix_timestamp=int(max_point["date"])
                )

        elif filter == Filter.MAX_TRANSACTIONS:
            if frequency == Frequency.HOUR:
                data = self.get_pair_hour_data(start_timestamp, end_timestamp)
                if not data:
                    return None
                max_point = max(data, key=lambda x: int(x["hourlyTxns"]))
                return TimeData(
                    block_number=0,
                    block_timestamp=int(max_point["hourStartUnix"]),
                    unix_timestamp=int(max_point["hourStartUnix"])
                )
            else:
                data = self.get_pair_day_data(start_timestamp, end_timestamp)
                if not data:
                    return None
                max_point = max(data, key=lambda x: int(x["dailyTxns"]))
                return TimeData(
                    block_number=0,
                    block_timestamp=int(max_point["date"]),
                    unix_timestamp=int(max_point["date"])
                )

        return None

    def get_eth_price(self) -> float:
        """Get current ETH price in USD from the Bundle entity."""
        query = """
        {
            bundle(id: "1") {
                ethPrice
            }
        }
        """
        data = self._query(query)
        bundle = data.get("bundle")
        if bundle:
            return float(bundle["ethPrice"])
        return 0.0
