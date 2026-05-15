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
                ("Engagement preset", render_data["engagement_preset_name"]),
                ("Cloud provider", render_data["cloud_provider_name"]),
                ("Target type", render_data["target_type"]),
                ("Testing window", render_data["testing_window"]),
                ("Production environment", "Yes" if render_data["production_environment"] else "No"),
                ("Authentication provided", "Yes" if render_data["authentication_provided"] else "No"),
            ],
        )

        self._add_paragraph(
            document,
            "This authorization letter confirms the security engagement may proceed under the documented operational boundaries.",
        )
        self._add_section(document, "Engagement objectives", render_data.get("objectives_list", [render_data.get("objectives_text", "")]))
        self._add_section(document, "Supported scope", render_data.get("scope_assets_list", [render_data.get("scope_text", "")]))

        if render_data.get("operational_notes"):
            self._add_section(document, "Operational notes", [render_data["operational_notes"]])

        self._add_section(document, "Authorization statement", [
            "The client has authorized the assessment activities described in the scope definition.",
            "Testing will remain aligned with jurisdiction requirements, cloud provider expectations, and client operational constraints.",
        ])
        self._add_section(document, "Approved testing statement", [
            "Permitted engagement activities are limited to the authorized assets and objectives.",
            "No actions outside the approved engagement should be taken without separate authorization.",
        ])
        self._add_paragraph(document, "Signatory approval", bold=True)
        self._add_paragraph(document, "Client representative: _________________________________")
        self._add_paragraph(document, "Assessment lead: _________________________________")
        self._add_paragraph(document, "Date: _________________________________")
        self._add_paragraph(document, "Disclaimer", bold=True)
        self._add_paragraph(
            document,
            "This document supports operational coordination and does not replace formal contractual terms.",
        )
        document.save(output_path)
        return output_path

    def generate_rules_of_engagement(self, render_data: dict, output_path: Path) -> Path:
        document = self._create_document()
        self._add_heading(document, "Rules of Engagement")
        self._add_paragraph(document, "This document defines the operational conditions and expectations for the engagement.")

        self._add_section(document, "Permitted activities", [
            "Testing authorized targets and assets within the documented engagement scope.",
            "Reviewing configuration, access control, and security posture.",
            "Reporting findings in clear and deterministic language.",
        ])
        if render_data.get("preset_roe_notes"):
            self._add_section(document, "Engagement guidance", render_data["preset_roe_notes"])

        self._add_section(document, "Prohibited activities", [
            "Unauthorized testing outside the defined scope.",
            "Denial-of-service techniques unless explicitly approved.",
            "Social engineering or physical security testing unless separately agreed.",
        ])

        self._add_section(document, "Communication expectations", [
            "The assessment team will provide timely status updates for critical findings.",
            "Communication will be coordinated through the designated client contact.",
            "All findings will be documented with operational context and impact statements.",
        ])

        self._add_section(document, "Escalation procedures", [
            "Significant issues will be escalated immediately to the client contact.",
            "Operational risks will be documented and reviewed without delay.",
            "Escalation will preserve evidence integrity and maintain transparency.",
        ])

        if render_data.get("testing_window"):
            self._add_section(document, "Testing window", [render_data["testing_window"]])
        if render_data.get("preset_testing_window"):
            self._add_section(document, "Recommended timing", [render_data["preset_testing_window"]])

        if render_data.get("preset_operational_considerations"):
            self._add_section(document, "Operational considerations", render_data["preset_operational_considerations"])

        document.save(output_path)
        return output_path

    def generate_scope_definition(self, render_data: dict, output_path: Path) -> Path:
        document = self._create_document()
        self._add_heading(document, "Scope Definition")
        self._add_paragraph(document, "This document describes the in-scope assets, exclusions, environment controls, and testing context.")

        self._add_key_value_table(
            document,
            [
                ("Client", render_data["client_name"]),
                ("Target type", render_data["target_type"]),
                ("Engagement preset", render_data["engagement_preset_name"]),
                ("Jurisdiction", render_data["jurisdiction_name"]),
                ("Cloud provider", render_data["cloud_provider_name"]),
            ],
        )

        if render_data.get("objectives_list"):
            self._add_section(document, "Engagement objectives", render_data["objectives_list"])

        if render_data.get("scope_assets_list"):
            self._add_section(document, "In-scope assets", render_data["scope_assets_list"])

        if render_data.get("exclusions_list"):
            self._add_section(document, "Exclusions", render_data["exclusions_list"])

        scope_metadata = [
            f"Testing window: {render_data['testing_window']}",
            f"Production environment: {'Yes' if render_data['production_environment'] else 'No'}",
            f"Authentication provided: {'Yes' if render_data['authentication_provided'] else 'No'}",
        ]
        self._add_section(document, "Engagement context", scope_metadata)

        if render_data.get("operational_notes"):
            self._add_section(document, "Operational notes", [render_data["operational_notes"]])

        self._add_section(document, "Cloud provider context", [
            f"Cloud provider: {render_data['cloud_provider_name']}",
            render_data.get("cloud_provider_summary", "No provider summary is available."),
        ])

        provider_controls = render_data.get("cloud_provider_controls", [])
        if provider_controls:
            self._add_section(document, "Cloud operational considerations", provider_controls)

        self._add_paragraph(document, "The scope definition supports operational planning, client agreement, and testing coordination.")
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
