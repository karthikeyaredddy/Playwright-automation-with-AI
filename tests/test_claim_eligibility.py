from pages.claim_eligibility_page import ClaimEligibilityPage


class TestClaimEligibility:

    def test_claim_eligibility_card_working(self, logged_in_page):

        claim = ClaimEligibilityPage(logged_in_page)

        assert claim.verify_claim_eligibility_card()