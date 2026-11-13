import pytest
from pages.claim_eligibility_page import ClaimEligibilityPage


@pytest.mark.order(3)
class TestClaimEligibility:

    def test_claim_eligibility_card_working(self, logged_in_page):

        claim = ClaimEligibilityPage(logged_in_page)

        assert claim.verify_claim_eligibility_card()

    def test_role_designation_configuration(self,logged_in_page ):
        claim = ClaimEligibilityPage(logged_in_page)

        assert claim.verify_role_designation_configuration()

    def test_add_claim_rule_for_existing_role(
            self,
            logged_in_page
    ):
        claim = ClaimEligibilityPage(
            logged_in_page
        )

        assert claim.add_claim_rule_for_existing_role()