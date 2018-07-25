# Checker 修改说明

1. 后续运行无法注册问题：`WebChecker` 类中成员变量 `self.username` 改为了 `self._generate_randstr()`；
2. 支付流程：由于在支付阶段设置了条件竞争漏洞，更改了部分支付逻辑。在 `shopcar_pay_test()` 与 `pay_test()` 的支付测试的过程中，增加了 `id` 字段，同时取消了随机的 `price`；
3. 密码重置流程：由于在密码重置阶段设置了逻辑漏洞，因此在 `pass_reset()` 中增加了 `username`、`password`、`password_confirm` 字段。

# Checker 使用方式

```
python checker.py 127.0.0.1 80 csrfmiddlewaretoken
```
