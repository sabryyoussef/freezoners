/** @odoo-module **/

import { Component } from '@odoo/owl';
import { useState } from '@odoo/owl/hooks';
import { registry } from '@odoo/owl/core';

class Many2ManyPdfPreview extends Component {
    setup() {
        this.state = useState({
            attachments: this.props.recordData.pdf_files.res_ids || []
        });
    }

    async renderPdfPreviews() {
        const attachments = this.state.attachments;
        for (const attachmentId of attachments) {
            // Fetch the attachment using attachmentId and render preview
            // Use PDF.js or any other library to render the preview
        }
    }

    mounted() {
        this.renderPdfPreviews();
    }
}

Many2ManyPdfPreview.template = 'client_documents.Many2ManyPdfPreview';

registry.category('components').add('Many2ManyPdfPreview', Many2ManyPdfPreview);

export default Many2ManyPdfPreview;
