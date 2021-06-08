# -*- coding: utf-8 -*-

from typing import Dict

import rule_engine

from goals.providers.haproxy import HAProxyProvider
from goals.rules.base import BaseRule


class DecreaseRateLimit(BaseRule):
    action_provider = HAProxyProvider()

    def __init__(self):
        self.context = rule_engine.Context(type_resolver=rule_engine.type_resolver_from_dict({
            'context_name': rule_engine.DataType.STRING,
        }))
        self.rule_str = 'context_name == "low_instances_haproxy"'
        self.rule = rule_engine.Rule(self.rule_str, context=self.context)

    def get_rule(self):
        return self.rule

    def is_rule_triggered(self, params: Dict):
        print(params)
        return self.rule.matches(params)

    def perform_action(self, payload={}):
        self.action_provider.replace_entry_to_map("ratelimit.map", "rate_limit", 4)

    def get_context(self):
        return self.context


class IncreaseRateLimit(BaseRule):
    action_provider = HAProxyProvider()

    def __init__(self):
        self.context = rule_engine.Context(type_resolver=rule_engine.type_resolver_from_dict({
            'context_name': rule_engine.DataType.STRING,
        }))
        self.rule_str = 'context_name == "high_instances_haproxy"'
        self.rule = rule_engine.Rule(self.rule_str, context=self.context)

    def get_rule(self):
        return self.rule

    def is_rule_triggered(self, params: Dict):
        return self.rule.matches(params)

    def perform_action(self, payload={}):
        self.action_provider.replace_entry_to_map("ratelimit.map", "rate_limit", 15)

    def get_context(self):
        return self.context