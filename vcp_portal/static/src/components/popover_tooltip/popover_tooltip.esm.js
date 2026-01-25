import {Component} from "@odoo/owl";

export class PopoverTooltip extends Component {
    static template = "vcp.PopoverTooltip";
    static props = {
        content: String,
    };
}
