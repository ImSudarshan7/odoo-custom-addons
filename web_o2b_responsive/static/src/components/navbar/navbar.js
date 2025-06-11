/** @odoo-module */

/**********************************************************************************
*
*    Copyright (c) 2017-today MuK IT GmbH.
*
*    This file is part of MuK Theme
*    (see https://mukit.at).
*
*    This program is free software: you can redistribute it and/or modify
*    it under the terms of the GNU Lesser General Public License as published by
*    the Free Software Foundation, either version 3 of the License, or
*    (at your option) any later version.
*
*    This program is distributed in the hope that it will be useful,
*    but WITHOUT ANY WARRANTY; without even the implied warranty of
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*    GNU Lesser General Public License for more details.
*
*    You should have received a copy of the GNU Lesser General Public License
*    along with this program. If not, see <http://www.gnu.org/licenses/>.
*
**********************************************************************************/

import { session } from "@web/session";
import { url } from "@web/core/utils/urls";
import { patch } from "@web/core/utils/patch";
import { registry } from "@web/core/registry";

import { NavBar } from "@web/webclient/navbar/navbar";

patch(NavBar.prototype, "web_o2b_responsive.NavBar", {
    setup() {
        this._super();
        if (session.theme_has_background_image) {
            this.backgroundImageUrl = url('/web/image', {
                model: 'res.company',
                field: 'background_image',
                id: this.env.services.company.currentCompany.id,
            });
        } else {
            this.backgroundImageUrl = '/web_o2b_responsive/static/src/img/pexels-photo.jpeg';
        }
    },
});
	