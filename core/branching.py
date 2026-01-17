import uuid
import copy

def new_branch(parent_branch="main"):
    return f"{parent_branch}_branch_{uuid.uuid4().hex[:4]}"

def fork_canon(canon, branch_id):
    clone = copy.deepcopy(canon)
    clone.active_branch = branch_id
    return clone
