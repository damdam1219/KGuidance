import praw
import os
import csv
from dotenv import load_dotenv

# ----------------------------
# 1️⃣ 환경 변수 로드
# ----------------------------
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

BASE_URL = "https://www.reddit.com"
SEARCH_QUERY = "korea travel OR korea trip OR seoul travel OR korea travel tips"
TARGET_SUBREDDIT = "KoreaTravel"

# ----------------------------
# 2️⃣ Reddit 크롤링 함수
# ----------------------------
def scrape_reddit_with_praw():
    try:
        print(f"✅ Reddit 로그인 성공! 현재 사용자: {reddit.user.me()}")
    except Exception as e:
        print(f"❌ Reddit 로그인 실패: {e}")
        return []

    results = []
    print(f"🔍 '{SEARCH_QUERY}' 검색 시작...")

    subreddit = reddit.subreddit(TARGET_SUBREDDIT)
    search_results = subreddit.search(
        query=SEARCH_QUERY,
        sort="relevance",
        time_filter="year"
    )

    for idx, submission in enumerate(search_results, 1):
        # 모든 댓글 가져오기
        submission.comments.replace_more(limit=None)
        comments_list = [c.body.strip() for c in submission.comments.list()]

        post_data = {
            "title": submission.title,
            "url": f"{BASE_URL}{submission.permalink}",
            "content": submission.selftext or "본문 없음",
            "comments": comments_list
        }

        results.append(post_data)

        # 게시물 및 댓글 수 실시간 출력
        print(f"[{idx}] '{submission.title}' 가져옴 | 댓글 수: {len(comments_list)}")

    print(f"\n📌 총 게시물 수: {len(results)}개")
    return results

# ----------------------------
# 3️⃣ CSV 저장
# ----------------------------
def save_to_csv(posts, filename="reddit_koreatravel_posts.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)  # ✅ 안전하게 따옴표 처리
        writer.writerow(["title", "url", "content", "comments"])  # 댓글은 리스트를 문자열로 저장
        for post in posts:
            comments_str = " ||| ".join(post["comments"])  # 댓글 구분자 |||
            writer.writerow([
                post["title"],
                post["url"],
                post["content"],
                comments_str
            ])
    print(f"✅ CSV 저장 완료: {filename}")

# ----------------------------
# 4️⃣ 메인 실행
# ----------------------------
if __name__ == "__main__":
    results = scrape_reddit_with_praw()
    save_to_csv(results)
