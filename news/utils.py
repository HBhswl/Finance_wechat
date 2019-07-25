def decode_label(_str):
    if not _str:
        return []
    labelList = _str.split('&')
    return labelList

def check_postLabel(_labelList):
    for label in _labelList:
        if 0 > int(label) or 90 < int(label):
            return False
    return True

def encode_label(_QuerySet):
    labels = []
    for obj in _QuerySet:
        labels.append(obj.label)
    labels = '&'.join(labels)
    return labels


def rank_post(_posts):
    ret = sorted(_posts, key=lambda post: post["weight"], reverse=True)
    return ret
