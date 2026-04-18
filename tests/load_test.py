from locust import HttpUser, task, between, events
import random


class TrendPulseUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.theme = random.choice(["ai tools", "crypto", "gaming", "fitness", "fashion"])
        self.platform = random.choice(["tiktok", "mobile", "steam"])
        self.region = random.choice(["global", "us", "eu"])
        self.budget_mode = random.choice(["balanced", "low_cost"])
        self.task_type = random.choice(["creative", "analysis", "reasoning"])

    @task(10)
    def generate_idea(self):
        payload = {
            "theme": self.theme,
            "platform": self.platform,
            "region": self.region,
            "budget_mode": self.budget_mode,
            "task_type": self.task_type,
        }
        with self.client.post(
            "/v1/generate",
            json=payload,
            catch_response=True,
            name="/v1/generate",
        ) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 429:
                response.success()
            else:
                response.failure(f"Got {response.status_code}")

    @task(1)
    def health_check(self):
        self.client.get("/health", name="/health")

    @task(1)
    def metrics(self):
        self.client.get("/metrics", name="/metrics")


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print(f"Load test starting: {environment.runner.target_user_count} users")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print(f"Load test finished. Total requests: {environment.stats.total.num_requests}")
