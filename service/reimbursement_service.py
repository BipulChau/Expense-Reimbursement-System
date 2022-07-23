from dao.reimbursement_dao import ReimbursementDao
from utility.reimbursent_format import ReimbursementUtility
from exception.user_name_not_found import UserNotFoundError


class ReimbursementService:
    @staticmethod
    def get_user_reimbursement(user_id):
        user_reimbursements = ReimbursementDao.get_user_reimbursement(user_id)
        print(user_reimbursements)
        user_reimbursements_formatted = ReimbursementUtility.reimbursement_format(user_reimbursements)

        return {f"Reimbursement details of {user_id}": user_reimbursements_formatted}

    @staticmethod
    def get_user_reimbursement_args(user_id, args):
        user_reimbursements = ReimbursementDao.get_user_reimbursement_args(user_id, args)
        user_reimbursements_formatted = ReimbursementUtility.reimbursement_format(user_reimbursements)

        return {f"Reimbursement details of {user_id}": user_reimbursements_formatted}

    @staticmethod
    def create_reimbursement(user_id, data):
        new_reimbursement = ReimbursementDao.create_reimbursement(user_id, data)
        if new_reimbursement:
            return new_reimbursement
        raise UserNotFoundError(f"Username {user_id} not found !!!")

    @staticmethod
    def update_reimbursement(user_id, data):
        reimb_id = data["reimb_id"]
        reimb_author = data["reimb_author"]
        status = data["status"]
        updated_reimbursement_row = ReimbursementDao.update_reimbursement(user_id, reimb_author, reimb_id, status)
        if status == "approved" or status == "denied":
            return updated_reimbursement_row
        elif status == "pending":
            return {"message": f"Cannot update back to {status} status"}
        elif updated_reimbursement_row:
            return updated_reimbursement_row

