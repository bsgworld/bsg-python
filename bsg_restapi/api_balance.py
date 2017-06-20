#!/usr/bin/env python3

from .api import Requester, Response


class BalanceAPI(Requester):
    def get(self):
        return Response(self.proceed('common', 'balance'))
