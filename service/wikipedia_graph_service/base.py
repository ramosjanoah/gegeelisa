# there is no commmon function yet
from env import env
from repository import redis
from model import *
from helper import *


class Base():
    def __init__():
        pass

    def set_cached_internal_references(self, node):
        if node is None:
            return 
        
        all_internal_references = []
        for ref in node.referenced_to:
            all_internal_references.append(ref)

        for ref in all_internal_references:
            redis.rpush(self.internal_reference_key(node.string_id), self.encode_internal_reference_id(ref))
        redis.expire(self.internal_reference_key(node.string_id), 300)


    def get_cached_internal_references(self, string_id, offset, limit):
        redis.expire(self.internal_reference_key(string_id), 300)
        reference_list = redis.lrange(self.internal_reference_key(string_id), offset, offset+limit-1)
        if len(reference_list) == 0:
            return None, -1
        result = []
        for ref in reference_list:
            reference_node = WikipediaNode.find_by_page_id(self.decode_internal_reference_id(ref.decode()))
            if reference_node is None:
                return None, -1
            result.append(reference_node)
        total = redis.llen(self.internal_reference_key(string_id))
        return result, total


    def encode_internal_reference_id(self, node):
        return "pid:{}".format(node.page_id)


    def decode_internal_reference_id(self, str_):
        return int(str_.split(':')[1])


    def internal_reference_key(self, string_id):
        return 'internal_reference_key:{}'.format(string_id)
