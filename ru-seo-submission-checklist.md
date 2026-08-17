# 俄语版网站（/ru/）搜索引擎提交与收录清单

> 适用对象：Tianyi Machinery 独立站（www.tianyimachine.com）俄语版 `/ru/` 目录
> 目标：让俄语用户在 **Yandex**（俄罗斯/俄语区主力）和 **Google** 用俄语搜索时能找到网站
> 配套文件：`sitemap-ru.xml`（17 个俄语 URL，含 ru/en/x-default 互链）、`robots.txt`（已引用该 sitemap）

---

## 一、推送前自检（必做）

- [ ] 代码已通过 GitHub Desktop 提交并 **Push** 到线上（Cloudflare Pages 重新部署完成）
- [ ] 线上可访问：https://www.tianyimachine.com/ru/ 及 https://www.tianyimachine.com/sitemap-ru.xml 均返回 200
- [ ] `sitemap-ru.xml` 通过 XML 校验（本机已用 Python 解析：17 个 `<loc>`、51 条 `xhtml:link` 互链，无错误）
- [ ] 全站 34 个 HTML 页（17 英文 + 17 俄语）均含 `hreflang="ru"`，且每对页面互链一致
- [ ] 每个俄语页头部有 `lang="ru"`、`og:locale="ru_RU"`、`canonical` 指向自身 `/ru/...`
- [ ] 俄语页内图片路径为 `../images/...`（位于 `/ru/` 下），英文页为 `images/...` 或 `/images/...`，无 404
- [ ] 俄语页与英文页均有语言切换按钮（RU 页 "EN" → `/`，EN 页 "RU" → `/ru/...`），用户在站内不跳出
- [ ] `robots.txt` 含 `Sitemap: https://www.tianyimachine.com/sitemap-ru.xml`

---

## 二、Yandex Webmaster（重点，俄语搜索主战场）

1. 打开 https://webmaster.yandex.com/ ，用账号登录（建议用绑定了网站的 Yandex 账号）。
2. **添加站点**：输入 `https://www.tianyimachine.com`（主域），按提示完成所有权验证。
   - 若之前已添加主域，直接进入该站点后台即可，无需重复添加。
3. **验证方式**：可选用 HTML 元标签（网站 `<head>` 中已有 Yandex 验证 meta，确认仍存在）；
   或上传 `yandex_*.html` 验证文件到站点根目录；或 DNS TXT 记录。
4. **提交俄语 Sitemap**：
   - 左侧菜单 → **索引** → **Sitemap 文件**（或「站点地图」）。
   - 添加 `https://www.tianyimachine.com/sitemap-ru.xml`，等待抓取。
5. **地域定位（Region / Территория）**：
   - 站点设置里将 **区域** 设为 **中国**（或目标市场：如俄罗斯买家为主，可设俄罗斯），
     帮助 Yandex 理解站点服务范围。
6. **排除/规范**：确认 `ru/` 页面 `canonical` 指向自身，避免与英文版争权重。
7. **监测**：
   - 「索引」→「索引化的页面数」查看 `/ru/` 页面是否被收录；
   - 「诊断」→「抓取时的错误」排查 404/重定向。
8. 可用 **Yandex Station / Yandex Search** 实测：搜索 `конвейерное оборудование Китай`、`ленточный конвейер купить` 等俄语关键词，看是否出现 `/ru/` 结果。

---

## 三、Google Search Console（补充覆盖）

1. 打开 https://search.google.com/search-console/ ，登录并选择对应资源（主域 `www.tianyimachine.com` 或 `sc-domain:tianyimachine.com`）。
2. **提交 Sitemap**：
   - 左侧 → **Sitemaps** → 输入 `sitemap-ru.xml` → 提交。
   - 状态变为「成功」后，可看到已发现/已编入索引的 URL 数。
3. **国际定位（hreflang）校验**：
   - 左侧 → **国际定位（International Targeting）** → 查看 hreflang 错误报告。
   - 重点关注：返回值「无返回值页（no return tags）」或「hreflang 冲突」。
   - 本站点每对页面已互链（ru ↔ en ↔ x-default），正常情况下无错误。
4. **URL 检查工具**：逐个粘贴 `/ru/products/belt-conveyor.html` 等，确认「网址已编入索引」。
5. **实效查询**：在 Google 用 `site:www.tianyimachine.com/ru/` 查看已收录的俄语页。

---

## 四、推送后建议节奏

- 第 1 天：提交两个 Sitemap，完成 Yandex 验证与区域设置。
- 第 3–7 天：复查抓取错误，修复任何 404（重点：`/ru/` 下图片/链接是否大小写正确——Cloudflare 区分大小写）。
- 第 2–4 周：观察 Yandex / Google 收录量与俄语关键词排名，必要时补充俄语博客文章（目前 `/ru/blog.html` 卡片仍指向英文文章，后续可补写俄语博文进一步增强）。
- 长期：保持 `/ru/` 与英文版内容同步更新，新增产品页时同步生成俄语版并加入 `sitemap-ru.xml`。

---

## 五、本次上线内容回顾

- 新增俄语页：`ru/factory.html`、`ru/certifications.html`
- 全站 17 个俄语页（首页 + 11 产品 + contact + blog + projects + factory + certifications）均含 hreflang 互链
- 全部 34 个页面（17 英 + 17 俄）双向语言切换，俄语用户全程留在 `/ru/` 内
- `sitemap-ru.xml` 扩至 17 条 URL，每条含 ru/en/x-default 互链
- `robots.txt` 已引用该 sitemap

---

## 六、GitHub Desktop 推送 Summary（可直接复制）

```
Add Russian (/ru/) factory & certifications pages: 17 RU pages total with
hreflang ru/en/x-default + RU/EN language switchers on all 34 pages;
regenerated sitemap-ru.xml (17 URLs, 51 xhtml:link alternates);
robots.txt already references it.
```
