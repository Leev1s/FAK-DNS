<div align="center">

# FAK-DNS 🌐

**给 AdGuard Home 用的中国域名 DNS 分流规则**

从上游域名列表生成可直接导入的上游 DNS 文件。命中列表的域名使用国内 DNS，其余域名使用你设置的默认 DNS。

[![规则生成](https://github.com/Leev1s/FAK-DNS/actions/workflows/convert.yml/badge.svg)](https://github.com/Leev1s/FAK-DNS/actions/workflows/convert.yml)
[![上游同步](https://github.com/Leev1s/FAK-DNS/actions/workflows/sync.yml/badge.svg)](https://github.com/Leev1s/FAK-DNS/actions/workflows/sync.yml)
[![Stars](https://img.shields.io/github/stars/Leev1s/FAK-DNS?style=flat)](https://github.com/Leev1s/FAK-DNS/stargazers)
[![最近更新](https://img.shields.io/github/last-commit/Leev1s/FAK-DNS/master?label=%E6%9C%80%E8%BF%91%E6%9B%B4%E6%96%B0)](https://github.com/Leev1s/FAK-DNS/commits/master)

[下载规则](https://raw.githubusercontent.com/Leev1s/FAK-DNS/master/converted/FAK-DNS.txt) · [自定义 DNS](#自定义-dns) · [本地组合示例](#本地组合示例adguard-home--mihomo)

</div>

## 🧭 先了解它做什么

FAK-DNS 基于 [dnsmasq-china-list](https://github.com/felixonmars/dnsmasq-china-list) 的域名列表，生成 [AdGuard Home 上游 DNS 文件](https://github.com/AdguardTeam/AdGuardHome/wiki/Configuration#loading-upstreams-from-file)。它只负责**选择 DNS 上游**：命中列表的域名使用 `CN_DNS`，其他域名使用 `THE_DNS`。默认配置分别使用阿里 DNS 和 Cloudflare DNS。

去广告需要在 AdGuard Home 中**另行启用 DNS 过滤规则**。FAK-DNS 不是广告过滤列表，也不根据访问者的 IP 所在地判断域名。

| 文件 | 用途 |
| --- | --- |
| [`converted/FAK-DNS.txt`](./converted/FAK-DNS.txt) | 含默认上游及全部域名规则，通常下载这一份 |
| [`converted/accelerated-domains.china.conf.txt`](./converted/accelerated-domains.china.conf.txt) | 中国域名规则 |
| [`converted/apple.china.conf.txt`](./converted/apple.china.conf.txt) | Apple 相关域名规则 |
| [`converted/google.china.conf.txt`](./converted/google.china.conf.txt) | Google 相关域名规则 |

> 💡 Apple 和 Google 的规则已包含在主文件中；单独的文件便于按需查看和使用。上游规则自动同步，生成任务每天运行，也支持手动运行。

## 🚀 快速使用

1. [下载主规则文件](https://raw.githubusercontent.com/Leev1s/FAK-DNS/master/converted/FAK-DNS.txt)，保存到运行 AdGuard Home 的设备，例如 `/opt/AdGuardHome/FAK-DNS.txt`。
2. 在 AdGuard Home 的 DNS 设置中，将该文件设为**上游 DNS 文件**。如需编辑 `AdGuardHome.yaml`，先停止服务，再设置：

   ```yaml
   dns:
     upstream_dns_file: /opt/AdGuardHome/FAK-DNS.txt
   ```

3. 启动 AdGuard Home，并按自己的需要在其过滤设置中添加、启用去广告规则。

> ⚠️ 设置了 `upstream_dns_file` 后，AdGuard Home 会使用文件中的上游设置，而不是配置中的 `upstream_dns` 列表。请确保文件中有可用的默认 DNS。[配置说明](https://github.com/AdguardTeam/AdGuardHome/wiki/Configuration#configuration-file)

## 🎛️ 自定义 DNS

想保留自己的下载地址，可以 fork 本仓库。进入 fork 的 **Settings → Secrets and variables → Actions → Variables**，创建两个仓库变量；**每行填写一个 DNS 地址**：

| 变量 | 作用 | 示例 |
| --- | --- | --- |
| `CN_DNS` | 域名列表命中时使用 | `https://dns.alidns.com/dns-query` |
| `THE_DNS` | 其他域名使用的默认上游 | `https://1.1.1.1/dns-query` |

例如，`CN_DNS` 可填写：

```text
https://dns.alidns.com/dns-query
tls://dns.alidns.com
```

`THE_DNS` 可填写：

```text
https://1.1.1.1/dns-query
https://1.0.0.1/dns-query
```

💡 两项都必须填写。支持 AdGuard Home 接受的普通 IP、DoH、DoT、DoQ 地址；`CN_DNS` 也兼容原先用空格分隔的写法。保存后到 **Actions → Convert Conf Files and Push to Repo → Run workflow** 手动生成一次。完成后，在**你自己的 fork** 的 `converted/FAK-DNS.txt` 下载规则；后续按计划自动更新。

## 🧩 本地组合示例：AdGuard Home + mihomo

适合两项服务运行在**同一台设备**的情况：AdGuard Home 接收设备的 DNS 请求并执行过滤；FAK-DNS 让列表内域名走国内 DNS；其他域名交给本地 mihomo DNS 的 fake-ip 模式处理。

```text
设备 → AdGuard Home（53 端口，过滤 + FAK-DNS 分流）
                         ├─ 列表内域名 → CN_DNS
                         └─ 其他域名 → mihomo DNS（127.0.0.1:1053，fake-ip）
```

1. 在你的 fork 中设置 `CN_DNS` 为国内 DNS；将 `THE_DNS` 设为 `127.0.0.1:1053`，然后手动运行生成任务。这个地址由 **AdGuard Home 所在设备**访问。
2. AdGuard Home 使用你 fork 生成的 `FAK-DNS.txt`，并单独启用需要的 DNS 过滤规则。
3. 在已有的 mihomo 配置中加入或调整 DNS 部分，例如：

   ```yaml
   dns:
     enable: true
     listen: 127.0.0.1:1053
     enhanced-mode: fake-ip
     fake-ip-range: 198.18.0.1/16
     default-nameserver:
       - 1.1.1.1
     nameserver:
       - https://1.1.1.1/dns-query
     fake-ip-filter:
       - '*.lan'
   ```

`nameserver` 请使用可独立访问的 DNS，**不要再指向 AdGuard Home**，否则会形成查询循环。只有转发给 mihomo 的域名会经过 fake-ip 处理；列表内域名直接使用 `CN_DNS`。不同设备部署时，把 `THE_DNS` 换成 mihomo DNS 的实际可达地址，并相应调整监听地址和访问控制。[mihomo DNS 配置说明](https://wiki.metacubex.one/config/dns/) · [AdGuard Home 上游文件说明](https://github.com/AdguardTeam/AdGuardHome/wiki/Configuration#loading-upstreams-from-file)

## 📜 来源与许可

域名列表来自 [felixonmars/dnsmasq-china-list](https://github.com/felixonmars/dnsmasq-china-list)，遵循 [WTFPL](./LICENSE-WTFPL)；本项目的新增内容遵循 [MIT](./LICENSE)。
