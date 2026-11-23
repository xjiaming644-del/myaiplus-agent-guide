# -*- coding: utf-8 -*-
"""Unit tests for public MyAIPlus agent onboarding guide generator & deliverables."""

from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from build_agent_kit import (  # noqa: E402
    COPYWRITING_FILENAME,
    MANUAL_FILENAME,
    README_FILENAME,
    WORKBENCH_FILENAME,
    ZIP_ROOT_FOLDER,
    AgentKitConfig,
    build_agent_kit,
)

GENERIC_FORBIDDEN_TERMS = (
    "单笔毛利",
    "毛利空间",
    "拿货底价",
    "factory_price",
    "user_price",
    "上一家",
)


class TestPublicAgentKit(unittest.TestCase):
    def test_build_outputs_web_docs_and_optional_zip(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            out_dir = tmp / "docs"
            web_out = tmp / "index.html"
            zip_out = tmp / "share.zip"
            outputs = build_agent_kit(
                AgentKitConfig(), out_dir=out_dir, zip_out=zip_out, web_out=web_out
            )

            expected_docs = (README_FILENAME, MANUAL_FILENAME, COPYWRITING_FILENAME)
            for fname in expected_docs:
                self.assertIn(fname, outputs)
                self.assertTrue(outputs[fname].is_file())
                self.assertGreater(outputs[fname].stat().st_size, 200)

            self.assertIn("web", outputs)
            self.assertTrue(web_out.is_file())
            self.assertGreater(web_out.stat().st_size, 10000)
            self.assertFalse((out_dir / WORKBENCH_FILENAME).exists())

            self.assertTrue(zip_out.is_file())
            expected_zip_members = {
                f"{ZIP_ROOT_FOLDER}/{README_FILENAME}",
                f"{ZIP_ROOT_FOLDER}/{MANUAL_FILENAME}",
                f"{ZIP_ROOT_FOLDER}/{COPYWRITING_FILENAME}",
                f"{ZIP_ROOT_FOLDER}/{WORKBENCH_FILENAME}",
            }
            with zipfile.ZipFile(zip_out, "r") as zf:
                self.assertEqual(set(zf.namelist()), expected_zip_members)
                self.assertEqual(
                    zf.read(f"{ZIP_ROOT_FOLDER}/{WORKBENCH_FILENAME}").decode("utf-8"),
                    web_out.read_text(encoding="utf-8"),
                )

    def test_generic_sanitization_no_internal_keywords(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            outputs = build_agent_kit(
                AgentKitConfig(),
                out_dir=tmp / "docs",
                zip_out=None,
                web_out=tmp / "index.html",
            )
            for label, path in outputs.items():
                text = path.read_text(encoding="utf-8")
                for bad in GENERIC_FORBIDDEN_TERMS:
                    self.assertNotIn(bad, text, f"Unexpected internal term '{bad}' in {label}")

    def test_plus_guide_structure_routes_13_steps_and_keywords(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            outputs = build_agent_kit(
                AgentKitConfig(),
                out_dir=tmp / "docs",
                zip_out=None,
                web_out=tmp / "index.html",
            )
            manual_text = outputs[MANUAL_FILENAME].read_text(encoding="utf-8")
            copy_text = outputs[COPYWRITING_FILENAME].read_text(encoding="utf-8")
            html_text = outputs["web"].read_text(encoding="utf-8")

            for marker in (
                'id="homeView"',
                'id="guideView"',
                'data-theme="dark"',
                'id="search"',
                'id="search2"',
                'id="profileDialog"',
                'id="coachBox"',
                'id="supportBtn"',
                'id="supportPanel"',
            ):
                self.assertIn(marker, html_text, f"Missing UI marker '{marker}'")

            data_match = re.search(
                r'<script\s+id="kit-data"\s+type="application/json">(.*?)</script>',
                html_text,
                re.DOTALL,
            )
            self.assertIsNotNone(data_match)
            data = json.loads(data_match.group(1).replace("<\\/", "</"))

            self.assertEqual(data["ownerWechat"], "xjmazh")
            self.assertEqual(data["defaultAgentFee"], "¥9.9")
            self.assertEqual(len(data["phases"]), 4)
            self.assertEqual(len(data["steps"]), 13)

            step_ids = [s["id"] for s in data["steps"]]
            self.assertEqual(len(set(step_ids)), 13)
            valid_ids = set(step_ids)

            for s in data["steps"]:
                self.assertTrue(0 <= s["phase"] < len(data["phases"]))
                self.assertTrue(isinstance(s.get("coach"), str) and s["coach"].strip())

            for rt in data["routes"]:
                for node in rt["steps"]:
                    self.assertIn(node["stepId"], valid_ids)

            for kw in (
                "xjmazh",
                "https://myaiplus.store/user/group/index",
                "¥9.9",
                "*.ns.cloudflare.com",
                "Tab 1",
                "Tab 2",
                "质保全程",
                "质保首登",
                "活动号无售后",
                "不提供也不推荐任何网络代理工具",
                "分站会员等级收入",
                "硬币",
                "5%",
                "95%",
                "¥9.41",
                "已绑定其他站点分销关系的会员不赠送",
            ):
                self.assertIn(kw, manual_text, f"Missing '{kw}' in manual")
                self.assertIn(kw, html_text, f"Missing '{kw}' in index.html")

            for ph in ("{{你的店铺名}}", "{{你的独立域名}}", "{{你的微信}}"):
                self.assertIn(ph, copy_text)
                self.assertIn(ph, html_text)

    def test_zero_external_assets_and_node_js_syntax(self) -> None:
        node_bin = shutil.which("node")
        self.assertIsNotNone(node_bin, "Node.js is required for JS syntax validation")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            outputs = build_agent_kit(
                AgentKitConfig(),
                out_dir=tmp / "docs",
                zip_out=None,
                web_out=tmp / "index.html",
            )
            html_text = outputs["web"].read_text(encoding="utf-8")

            self.assertIsNone(re.search(r"<script[^>]+src=['\"]https?://", html_text, re.IGNORECASE))
            self.assertIsNone(re.search(r"<link[^>]+href=['\"]https?://", html_text, re.IGNORECASE))
            self.assertNotIn("@import", html_text.lower())

            js_blocks = re.findall(r"<script>\s*(.*?)\s*</script>", html_text, re.DOTALL)
            self.assertGreaterEqual(len(js_blocks), 2)
            for idx, js_src in enumerate(js_blocks):
                js_file = tmp / f"inline_{idx}.js"
                js_file.write_text(js_src, encoding="utf-8")
                proc = subprocess.run(
                    [node_bin, "--check", str(js_file)],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                )
                self.assertEqual(proc.returncode, 0, f"node --check failed:\n{proc.stderr}")

    def test_custom_config_replaces_all_defaults(self) -> None:
        custom = AgentKitConfig(
            brand="NovaAI严选",
            store_url="https://novaai.example",
            agent_upgrade_url="https://novaai.example/user/group/index",
            owner_wechat="nova_custom_wx",
            agent_fee="¥29.9",
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            outputs = build_agent_kit(
                custom,
                out_dir=tmp / "docs",
                zip_out=tmp / "share.zip",
                web_out=tmp / "index.html",
            )
            for key in (README_FILENAME, MANUAL_FILENAME, COPYWRITING_FILENAME, "web"):
                content = outputs[key].read_text(encoding="utf-8")
                self.assertIn("nova_custom_wx", content)
                self.assertIn("¥29.9", content)
                self.assertIn("NovaAI严选", content)
                self.assertNotIn("xjmazh", content)
                self.assertNotIn("¥9.9", content)
                self.assertNotIn("myaiplus.store", content)


if __name__ == "__main__":
    unittest.main()
