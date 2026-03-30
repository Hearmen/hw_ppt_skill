#!/usr/bin/env python3
"""Extract a PPTX template's slide structure into a layout contract JSON file.

Usage:
    python scripts/extract_layout_contract.py template_unpacked/
    python scripts/extract_layout_contract.py template_unpacked/ -o layout/template_contract.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
    "p14": "http://schemas.microsoft.com/office/powerpoint/2010/main",
}

EMU_PER_INCH = 914400


def emu_to_inches(value: str | None) -> float | None:
    if value is None:
        return None
    return round(int(value) / EMU_PER_INCH, 3)


def text_content(node: ET.Element) -> str:
    parts = [t.text.strip() for t in node.findall(".//a:t", NS) if t.text and t.text.strip()]
    return " ".join(parts)


def get_cnvpr(node: ET.Element) -> tuple[int | None, str | None]:
    cnvpr = node.find("./p:nvSpPr/p:cNvPr", NS)
    if cnvpr is None:
        cnvpr = node.find("./p:nvPicPr/p:cNvPr", NS)
    if cnvpr is None:
        cnvpr = node.find("./p:nvGraphicFramePr/p:cNvPr", NS)
    if cnvpr is None:
        cnvpr = node.find("./p:nvCxnSpPr/p:cNvPr", NS)
    if cnvpr is None:
        return None, None
    shape_id = cnvpr.get("id")
    return (int(shape_id) if shape_id is not None else None, cnvpr.get("name"))


def get_placeholder(node: ET.Element) -> dict | None:
    ph = node.find("./p:nvSpPr/p:nvPr/p:ph", NS)
    if ph is None:
        return None
    return {
        "type": ph.get("type", "body"),
        "idx": ph.get("idx"),
        "size": ph.get("sz"),
    }


def get_geometry(node: ET.Element) -> dict | None:
    xfrm = node.find("./p:spPr/a:xfrm", NS)
    if xfrm is None:
        xfrm = node.find("./p:xfrm", NS)
    if xfrm is None:
        xfrm = node.find("./p:pic/p:spPr/a:xfrm", NS)
    if xfrm is None:
        return None

    off = xfrm.find("./a:off", NS)
    ext = xfrm.find("./a:ext", NS)
    if off is None or ext is None:
        return None

    return {
        "x": emu_to_inches(off.get("x")),
        "y": emu_to_inches(off.get("y")),
        "w": emu_to_inches(ext.get("cx")),
        "h": emu_to_inches(ext.get("cy")),
    }


def classify_element(node: ET.Element) -> str:
    tag = node.tag.split("}", 1)[-1]
    if tag == "sp":
        placeholder = get_placeholder(node)
        if placeholder:
            return "placeholder"
        if node.find("./p:nvSpPr/p:cNvSpPr[@txBox='1']", NS) is not None:
            return "text_box"
        return "shape"
    if tag == "pic":
        return "picture"
    if tag == "graphicFrame":
        return "graphic_frame"
    if tag == "cxnSp":
        return "connector"
    return tag


def recommend_action(element_type: str, sample_text: str, placeholder: dict | None) -> str:
    if placeholder is not None:
        return "replace_placeholder_content"
    if element_type == "text_box" and sample_text:
        return "replace_text_or_keep_as_fixed_label"
    if element_type in {"picture", "graphic_frame"}:
        return "review_if_visual_should_be_kept"
    return "preserve_unless_layout_needs_adjustment"


def load_relationship_map(rels_path: Path) -> dict[str, str]:
    root = ET.parse(rels_path).getroot()
    rel_map: dict[str, str] = {}
    for rel in root.findall("./pr:Relationship", NS):
        rel_id = rel.get("Id")
        target = rel.get("Target")
        if rel_id and target:
            rel_map[rel_id] = target
    return rel_map


def load_section_map(presentation_root: ET.Element) -> dict[int, str]:
    section_map: dict[int, str] = {}
    for section in presentation_root.findall(".//p14:section", NS):
        name = section.get("name")
        if not name:
            continue
        for slide_ref in section.findall("./p14:sldIdLst/p14:sldId", NS):
            slide_id = slide_ref.get("id")
            if slide_id is not None:
                section_map[int(slide_id)] = name
    return section_map


def extract_contract(unpacked_dir: Path) -> dict:
    presentation_path = unpacked_dir / "ppt" / "presentation.xml"
    rels_path = unpacked_dir / "ppt" / "_rels" / "presentation.xml.rels"

    presentation_root = ET.parse(presentation_path).getroot()
    rel_map = load_relationship_map(rels_path)
    section_map = load_section_map(presentation_root)

    slide_size = presentation_root.find("./p:sldSz", NS)
    slides = []

    for index, sld in enumerate(presentation_root.findall("./p:sldIdLst/p:sldId", NS), start=1):
        slide_id = int(sld.get("id"))
        rel_id = sld.get(f"{{{NS['r']}}}id")
        if rel_id is None or rel_id not in rel_map:
            continue

        slide_target = rel_map[rel_id]
        slide_file = Path("ppt") / slide_target
        slide_root = ET.parse(unpacked_dir / slide_file).getroot()
        sp_tree = slide_root.find("./p:cSld/p:spTree", NS)
        if sp_tree is None:
            continue

        elements = []
        for draw_order, node in enumerate(list(sp_tree)[2:], start=1):
            element_type = classify_element(node)
            placeholder = get_placeholder(node)
            sample_text = text_content(node)
            shape_id, name = get_cnvpr(node)
            geometry = get_geometry(node)

            elements.append(
                {
                    "order": draw_order,
                    "shape_id": shape_id,
                    "name": name,
                    "element_type": element_type,
                    "geometry_inches": geometry,
                    "placeholder": placeholder,
                    "sample_text": sample_text or None,
                    "recommended_action": recommend_action(element_type, sample_text, placeholder),
                }
            )

        slides.append(
            {
                "index": index,
                "slide_id": slide_id,
                "section_name": section_map.get(slide_id),
                "slide_file": slide_file.as_posix(),
                "element_count": len(elements),
                "elements": elements,
            }
        )

    return {
        "meta": {
            "template_unpacked_dir": str(unpacked_dir),
            "slide_size_inches": {
                "w": emu_to_inches(slide_size.get("cx") if slide_size is not None else None),
                "h": emu_to_inches(slide_size.get("cy") if slide_size is not None else None),
            },
            "total_slides": len(slides),
        },
        "slides": slides,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract PPTX template layout contract JSON")
    parser.add_argument("unpacked_dir", help="Path to an unpacked PPTX directory")
    parser.add_argument("-o", "--output", help="Write JSON to this file instead of stdout")
    args = parser.parse_args()

    unpacked_dir = Path(args.unpacked_dir)
    contract = extract_contract(unpacked_dir)
    payload = json.dumps(contract, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
