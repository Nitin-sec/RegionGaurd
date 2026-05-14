from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Inches, Pt

from ..utils.file_utils import ensure_directory_exists


class DocxGenerator:
    """Create professional DOCX deliverables for RegionGuard engagements."""

    def __init__(self, output_dir: Path):
        self.output_dir = ensure_directory_exists(output_dir)

    def generate_all(self, render_data: dict, base_name: str) -> list[Path]:
        files = [
            self.generate_authorization_letter(render_data, self.output_dir / f"{base_name}_authorization.docx"),
            self.generate_rules_of_engagement(render_data, self.output_dir / f"{base_name}_roe.docx"),
            self.generate_scope_definition(render_data, self.output_dir / f"{base_name}_scope.docx"),
        ]
        return files

    def generate_authorization_letter(self, render_data: dict, output_path: Path) -> Path:
        document = self._create_document()
        self._add_heading(document, "Authorization Letter")
        self._add_key_value_table(
            document,
            [
                ("Client", render_data["client_name"]),
                ("Document date", date.today().strftime("%B %d, %Y")),
                ("Jurisdiction", render_data["jurisdiction_name"]),
                ("Engagement type", render_data["roe_preset_name"]),
                ("Cloud provider", render_data["cloud_provider_name"]),
                ("Target type", render_data["target_type"]),
            ],
        )

        self._add_paragraph(
            document,
            "This document confirms the engagement is authorized to proceed with the defined scope and objectives.",
        )
        self._add_paragraph(
            document,
            "The assessment will follow agreed operational controls and is limited to the assets and environment described in the scope definition.",
        )
        self._add_section(document, "Authorization statement", [
            "The client has authorized the security assessment and accepts that testing will be carried out within the stated boundaries.",
            "Testing execution will remain consistent with stated scope, jurisdiction requirements, and cloud provider context.",
        ])
        self._add_section(document, "Approved testing statement", [
            "Approved techniques include discovery, configuration review, and controlled testing of authorized targets.",
            "No destructive actions will be performed without explicit, separate authorization.",
        ])
        self._add_section(document, "Scope summary", [render_data["scope_text"]])
        self._add_paragraph(document, "Signatory approval", bold=True)
        self._add_paragraph(document, "Client representative: _________________________________")
        self._add_paragraph(document, "Assessment lead: _________________________________")
        self._add_paragraph(document, "Date: _________________________________")
        self._add_paragraph(document, "Disclaimer", bold=True)
        self._add_paragraph(
            document,
            "This document is intended for engagement planning and operational coordination. It is not legal advice.",
        )
        document.save(output_path)
        return output_path

    def generate_rules_of_engagement(self, render_data: dict, output_path: Path) -> Path:
        document = self._create_document()
        self._add_heading(document, "Rules of Engagement")
        self._add_paragraph(document, "This document defines the conditions and expectations for the engagement.")

        self._add_section(document, "Permitted activities", [
            "Testing authorized targets and assets within the documented scope.",
            "Reviewing configuration, access control, and security monitoring posture.",
            "Providing concise operational findings and improvement recommendations.",
        ])
        if render_data.get("roe_guidance"):
            self._add_section(document, "Engagement guidance", render_data["roe_guidance"])

        self._add_section(document, "Prohibited activities", [
            "Unauthorized testing outside the defined scope.",
            "Denial-of-service techniques unless explicitly approved.",
            "Social engineering and physical security testing unless separately agreed.",
        ])

        self._add_section(document, "Communication expectations", [
            "The assessment team will provide regular status updates for critical findings.",
            "Communication will be routed through the designated client contact and assessment lead.",
            "All findings will be reported clearly and without speculative language.",
        ])

        self._add_section(document, "Escalation procedures", [
            "Significant issues will be escalated to the client contact immediately.",
            "Operational risks that impact the engagement will be documented and reviewed without delay.",
            "Escalation will maintain transparency and preserve evidence integrity.",
        ])

        report_timing = render_data.get("roe_report_timing")
        if report_timing:
            self._add_section(document, "Reporting timeline", [report_timing])

        scope_limitations = render_data.get("roe_scope_limitations")
        if scope_limitations:
            self._add_section(document, "Testing limitations", [scope_limitations])

        document.save(output_path)
        return output_path

    def generate_scope_definition(self, render_data: dict, output_path: Path) -> Path:
        document = self._create_document()
        self._add_heading(document, "Scope Definition")
        self._add_paragraph(document, "This document describes what is in scope, what is excluded, and the supporting cloud context.")

        self._add_key_value_table(
            document,
            [
                ("Client", render_data["client_name"]),
                ("Target type", render_data["target_type"]),
                ("Jurisdiction", render_data["jurisdiction_name"]),
                ("Cloud provider", render_data["cloud_provider_name"]),
            ],
        )

        self._add_section(document, "In-scope assets", [
            render_data["scope_text"],
            "Assets and systems described in the scope are included unless otherwise noted.",
        ])

        exclusions = [
            "Assets not explicitly included in the scope statement.",
            "Third-party systems outside the approved cloud provider boundary.",
        ]
        if render_data.get("roe_scope_limitations"):
            exclusions.append(render_data["roe_scope_limitations"])

        self._add_section(document, "Exclusions", exclusions)

        self._add_section(document, "Cloud provider context", [
            f"Cloud provider: {render_data['cloud_provider_name']}",
            render_data.get("cloud_provider_summary", "No provider summary is available."),
        ])

        provider_controls = render_data.get("cloud_provider_controls", [])
        if provider_controls:
            self._add_section(document, "Operational considerations", provider_controls)

        self._add_paragraph(document, "The scope definition is designed to support operational planning, status tracking, and clear client handoff.")
        document.save(output_path)
        return output_path

    def _create_document(self) -> Document:
        document = Document()
        style = document.styles["Normal"]
        style.font.name = "Calibri"
        style.font.size = Pt(11)
        style.paragraph_format.space_after = Pt(6)
        return document

    def _add_heading(self, document: Document, text: str, level: int = 1) -> None:
        paragraph = document.add_paragraph()
        run = paragraph.add_run(text)
        run.bold = True
        run.font.size = Pt(18 if level == 1 else 14)
        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        paragraph.space_after = Pt(12)

    def _add_paragraph(self, document: Document, text: str, bold: bool = False) -> None:
        paragraph = document.add_paragraph(text)
        run = paragraph.runs[0]
        run.bold = bold
        paragraph.space_after = Pt(8)

    def _add_section(self, document: Document, heading: str, points: list[str]) -> None:
        self._add_paragraph(document, heading, bold=True)
        for item in points:
            self._add_bullet(document, item)

    def _add_bullet(self, document: Document, text: str) -> None:
        paragraph = document.add_paragraph(text, style="List Bullet")
        paragraph.paragraph_format.left_indent = Inches(0.25)
        paragraph.paragraph_format.space_after = Pt(4)

    def _add_key_value_table(self, document: Document, rows: list[tuple[str, str]]) -> None:
        table = document.add_table(rows=0, cols=2)
        table.style = "LightShading-Accent1"
        for label, value in rows:
            row = table.add_row().cells
            row[0].text = label
            row[1].text = value
            row[0].paragraphs[0].runs[0].bold = True
        table.autofit = True
        document.add_paragraph()
