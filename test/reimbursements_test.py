import pytest

import dao.reimbursement_dao
from service.reimbursement_service import ReimbursementService
from dao.reimbursement_dao import ReimbursementDao


def test_get_user_reimbursement(mocker):
    # Arrange
    def mock_get_user_reimbursement(user_id):
        if user_id == "mahwish44":
            return [[6, 3000.00, "Fri, 22 Jul 2022 14:55:35 GMT", None, 'pending', 'other', 'Vacation', '"/Users/bipulchaudhary/Desktop/receipt.jpg"', 'mahwish44', 'bipul513']]
    mocker.patch("dao.reimbursement_dao.ReimbursementDao.get_user_reimbursement", mock_get_user_reimbursement)

    # Act
    actual = ReimbursementService.get_user_reimbursement("mahwish44")

    # Assert
    var = actual == {
        "Reimbursement details of mahwish44": [
            {
                "description": "Vacation",
                "receipt_img": "\"/Users/bipulchaudhary/Desktop/receipt.jpg\"",
                "reimb_author": "mahwish44",
                "reimb_id": 6,
                "reimb_resolver": "bipul513",
                "reimbursement_amount": "3000.00",
                "resolved_at": None,
                "status": "pending",
                "submitted_at": "Fri, 22 Jul 2022 14:55:35 GMT",
                "type_of_expense": "other"
            }
            ]
    }