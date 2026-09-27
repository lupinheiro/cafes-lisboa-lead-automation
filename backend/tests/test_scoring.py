from app.services.scoring.scorer import score_lead


def test_score_lead_base_case_has_no_extra_signals() -> None:
    lead = {"website": None, "rating": None, "phone": None}
    assert score_lead(lead) == 40.0


def test_score_lead_rewards_website_and_phone() -> None:
    lead = {"website": "https://example.com", "rating": None, "phone": "+351123456789"}
    assert score_lead(lead) == 70.0


def test_score_lead_full_signals() -> None:
    lead = {"website": "https://example.com", "rating": 4.5, "phone": "+351123456789"}
    assert score_lead(lead) == 97.0


def test_score_lead_caps_at_one_hundred() -> None:
    lead = {"website": "https://example.com", "rating": 5.0, "phone": "+351123456789"}
    assert score_lead(lead) == 100.0
