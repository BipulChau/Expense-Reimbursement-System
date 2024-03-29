import pytest

import dao.reimbursement_dao
from service.reimbursement_service import ReimbursementService
from dao.reimbursement_dao import ReimbursementDao


def test_get_user_reimbursement(mocker):
    # Arrange
    def mock_get_user_reimbursement(user_id):
        if user_id == "mahwish44":
            return [[6, 3000.00, "Fri, 22 Jul 2022 14:55:35 GMT", None, 'pending', 'other', 'Vacation',
                     '"/Users/bipulchaudhary/Desktop/receipt.jpg"', 'mahwish44', 'bipul513']]

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


def test_get_user_reimbursement_args(mocker):
    #  Arrange
    def mock_get_user_reimbursement_args(user_id, args):
        if user_id == "shaquera7" and args == "denied":
            return [[7, 200.00, "Tue, 26 Jul 2022 15:42:47 GMT", "Wed, 27 Jul 2022 15:52:16 GMT", 'denied', 'Lodging',
                     'Foof', None, 'shaquera7', 'bipul513']]

    mocker.patch("dao.reimbursement_dao.ReimbursementDao.get_user_reimbursement_args", mock_get_user_reimbursement_args)

    # ACT
    actual = ReimbursementService.get_user_reimbursement_args("shaquera7", "denied")

    # Assert
    var = actual == {
        "Reimbursement details of shaquera7": [
            {
                "description": "Foof",
                "receipt_img": None,
                "reimb_author": "shaquera7",
                "reimb_id": 7,
                "reimb_resolver": "bipul513",
                "reimbursement_amount": "200.00",
                "resolved_at": "Wed, 27 Jul 2022 15:52:16 GMT",
                "status": "denied",
                "submitted_at": "Tue, 26 Jul 2022 15:42:47 GMT",
                "type_of_expense": "Lodging"
            }
        ]
    }


def test_create_reimbursement(mocker):
    # Arrange
    def mock_create_reimbursement(user_id, data):
        if user_id == "shaquera7" and data == {'reimbursement_amount': 100, 'type_of_expense': 'Food',
                                               'description': 'Client Visit',
                                               'receipt_img': '/Users/bipulchaudhary/Desktop/receipt.jpg'}:
            return "New reimbursement successfully created"

    mocker.patch("dao.reimbursement_dao.ReimbursementDao.create_reimbursement", mock_create_reimbursement)

    # Act
    data1 = {'reimbursement_amount': 100, 'type_of_expense': 'Food',
             'description': 'Client Visit',
             'receipt_img': '/Users/bipulchaudhary/Desktop/receipt.jpg'}
    actual = ReimbursementService.create_reimbursement("shaquera7", data1)

    # Assert
    actual == "New reimbursement successfully created"


def test_update_reimbursement(mocker):
    # Arrange
    def mock_update_reimbursement(user_id, reimb_author, reimb_id, status):
        if user_id == "bipul513" and reimb_author == "shaquera7" and reimb_id == 8 and status == "approved":
            return {"message": f"Reimbursement request having reimbursement id number 8 of shaquera7 has been approved"}

    mocker.patch("dao.reimbursement_dao.ReimbursementDao.update_reimbursement", mock_update_reimbursement)

    # Act
    data1 = {'reimb_id': '8', 'reimb_author': 'shaquera7', 'status': 'approved'}

    actual = ReimbursementService.update_reimbursement("bipul513", data1)

    # Assert
    var = actual == {
        "message": "Reimbursement request having reimbursement id number 8 of shaquera7 has been approved"
    }
