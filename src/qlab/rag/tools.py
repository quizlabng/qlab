from langchain_core.tools import tool
from .schemas import GetUserSubjectRank, GetUserSubjectPoints, GetUserSubjectStats
from .database import redis_client


@tool(args_schema=GetUserSubjectRank)
def get_user_subject_rank(user_id: str, subject: str) -> int | None:
    """Get a user's rank for a given subject."""
    rank = redis_client.zrevrank(f"leaderboard:{subject}", user_id)
    return int(rank) + 1 if rank is not None else None


@tool(args_schema=GetUserSubjectPoints)
def get_user_subject_points(user_id: str, subject: str) -> int | None:
    """Get a user's total points for a given subject."""
    points = redis_client.hget(f"user:{user_id}:stats:{subject}", "total_points")
    return int(points) if points is not None else None


@tool(args_schema=GetUserSubjectStats)
def get_user_subject_stats(user_id: str, subject: str) -> dict:
    """Get a user's rank and total points for a given subject."""
    rank = get_user_subject_rank.invoke({"user_id": user_id, "subject": subject})
    if rank is None:
        return None

    points = get_user_subject_points.invoke({"user_id": user_id, "subject": subject})
    return {
        "rank": rank,
        "total_points": points if points is not None else 0,
    }


tools = [get_user_subject_rank, get_user_subject_points, get_user_subject_stats]
tools_map = {tool.name: tool for tool in tools}


if __name__ == "__main__":
    stats = get_user_subject_stats.invoke({"user_id": "1575156816", "subject": "chemistry"})
    print(stats)