odoo.define('website_teams.partner_assign', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var time = require('web.time');

publicWidget.registry.crmPartnerAssign = publicWidget.Widget.extend({
    selector: '#wrapwrap:has(.interested_partner_assign_form, .desinterested_partner_assign_form, .team-stage-button, .new_team_form)',
    events: {
        'click .interested_partner_assign_confirm': '_onInterestedPartnerAssignConfirm',
        'click .desinterested_partner_assign_confirm': '_onDesinterestedPartnerAssignConfirm',
        'click .team-stage-button': '_onTeamStageButtonClick',
        'change .edit_contact_form .country_id': '_onEditContactFormChange',
        'click .edit_contact_confirm': '_onEditContactConfirm',
        'click .new_team_confirm': '_onNewTeamConfirm',
        'click .edit_opp_confirm': '_onEditOppConfirm',
        'change .edit_opp_form .next_activity': '_onChangeNextActivity',
        'click div.input-group span.fa-calendar': '_onCalendarIconClick',
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {jQuery} $btn
     * @param {function} callback
     * @returns {Promise}
     */
    _buttonExec: function ($btn, callback) {
        // TODO remove once the automatic system which does this lands in master
        $btn.prop('disabled', true);
        return callback.call(this).guardedCatch(function () {
            $btn.prop('disabled', false);
        });
    },
    /**
     * @private
     * @returns {Promise}
     */
//    _confirmInterestedPartner: function () {
//        return this._rpc({
//            model: 'crm.lead',
//            method: 'partner_interested',
//            args: [
//                [parseInt($('.interested_partner_assign_form .assign_lead_id').val())],
//                $('.interested_partner_assign_form .comment_interested').val()
//            ],
//        }).then(function () {
//            window.location.href = '/my/leads';
//        });
//    },
    /**
     * @private
     * @returns {Promise}
     */
//    _confirmDesinterestedPartner: function () {
//        return this._rpc({
//            model: 'crm.lead',
//            method: 'partner_desinterested',
//            args: [
//                [parseInt($('.desinterested_partner_assign_form .assign_lead_id').val())],
//                $('.desinterested_partner_assign_form .comment_desinterested').val(),
//                $('.desinterested_partner_assign_form .contacted_desinterested').prop('checked'),
//                $('.desinterested_partner_assign_form .customer_mark_spam').prop('checked'),
//            ],
//        }).then(function () {
//            window.location.href = '/my/leads';
//        });
//    },
    /**
     * @private
     * @param {}
     * @returns {Promise}
     */
//    _changeTeamStage: function (TeamID, stageID) {
//        return this._rpc({
//            model: 'team.team',
//            method: 'write',
//            args: [[TeamID], {
//                stage_id: stageID,
//            }],
//            context: _.extend({website_partner_assign: 1}),
//        }).then(function () {
//            window.location.reload();
//        });
//    },
    /**
     * @private
     * @returns {Promise}
     */
    _editContact: function () {
//        alert('edit!!')
//        return;
        return this._rpc({
            model: 'team.team',
            method: 'write',
            args: [[parseInt($('.edit_contact_form .team_id').val())], {
                partner_name: $('.edit_contact_form .partner_name').val(),
                phone: $('.edit_contact_form .phone').val(),
                mobile: $('.edit_contact_form .mobile').val(),
                email_from: $('.edit_contact_form .email_from').val(),
                street: $('.edit_contact_form .street').val(),
                street2: $('.edit_contact_form .street2').val(),
                city: $('.edit_contact_form .city').val(),
                zip: $('.edit_contact_form .zip').val(),
                state_id: parseInt($('.edit_contact_form .state_id').find(':selected').attr('value')),
                country_id: parseInt($('.edit_contact_form .country_id').find(':selected').attr('value')),
            }],
        }).then(function () {
            window.location.reload();
        });
    },


    /**
     * @private
     * @returns {Promise}
     */
    _createTeam: function () {
        return this._rpc({
            model: 'team.team',
            method: 'create_team_portal',
            args: [{
                title: $('.new_team_form .title').val(),
            }],
        }).then(function (response) {
            if (response.errors) {
                $('#new-team-dialog .alert').remove();
                $('#new-team-dialog div:first').prepend('<div class="alert alert-danger">' + response.errors + '</div>');
                return Promise.reject(response);
            } else {
                window.location = '/my/team/' + response.id;
            }
        });
    },
    /**
     * @private
     * @returns {Promise}
     */
    _editTeam: function () {

        return this._rpc({
            model: 'team.team',
            method: 'update_team_portal',
            args: [[parseInt($('.edit_opp_form .team_id').val())], {
                name: $('.edit_opp_form .name').val(),
                users: [
                    $('input[name="post_user_1"]').val(),
                    $('input[name="post_user_2"]').val(),
                    $('input[name="post_user_3"]').val(),
                    $('input[name="post_user_4"]').val(),
                ],
            }],
        }).then(function () {
            window.location.reload();
        });
    },

    _onChangeNextActivity: function (ev) {
        var $selected = $('.edit_opp_form .next_activity').find(':selected');
        if ($selected.attr('activity_summary')) {
            $('.edit_opp_form .activity_summary').val($selected.attr('activity_summary'));
        }
        if ($selected.attr('delay_count')) {
            var now = moment();
            var date = now.add(parseInt($selected.attr('delay_count')), $selected.attr('delay_unit'));
            $('.edit_opp_form .activity_date_deadline').val(date.format(time.getLangDateFormat()));
        }
    },


    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {Event} ev
     */
//    _onInterestedPartnerAssignConfirm: function (ev) {
//        ev.preventDefault();
//        ev.stopPropagation();
//        if ($('.interested_partner_assign_form .comment_interested').val() && $('.interested_partner_assign_form .contacted_interested').prop('checked')) {
//            this._buttonExec($(ev.currentTarget), this._confirmInterestedPartner);
//        } else {
//            $('.interested_partner_assign_form .error_partner_assign_interested').css('display', 'block');
//        }
//    },
    /**
     * @private
     * @param {Event} ev
     */
//    _onDesinterestedPartnerAssignConfirm: function (ev) {
//        ev.preventDefault();
//        ev.stopPropagation();
//        this._buttonExec($(ev.currentTarget), this._confirmDesinterestedPartner);
//    },
    /**
     * @private
     * @param {Event} ev
     */
//    _onTeamStageButtonClick: function (ev) {
//        var $btn = $(ev.currentTarget);
//        this._buttonExec(
//            $btn,
//            this._changeTeamStage.bind(this, parseInt($btn.attr('team')), parseInt($btn.attr('data')))
//        );
//    },
    /**
     * @private
     * @param {Event} ev
     */
    _onEditContactFormChange: function (ev) {
        console.log('test')
        var countryID = $('.edit_contact_form .country_id').find(':selected').attr('value');
        $('.edit_contact_form .state[country!=' + countryID + ']').css('display', 'none');
        $('.edit_contact_form .state[country=' + countryID + ']').css('display', 'block');
    },
    /**
     * @private
     * @param {Event} ev
     */
    _onEditContactConfirm: function (ev) {
        console.log('te')
        ev.preventDefault();
        ev.stopPropagation();
        this._buttonExec($(ev.currentTarget), this._editContact);
    },
    /**
     * @private
     * @param {Event} ev
     */
    _onNewTeamConfirm: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        this._buttonExec($(ev.currentTarget), this._createTeam);
    },
    /**
     * @private
     * @param {Event} ev
     */
    _onEditOppConfirm: function (ev) {
        alert('editoppconfirm')

        ev.preventDefault();
        ev.stopPropagation();
        return;
        if ($(".edit_opp_form")[0].checkValidity()) {
            this._buttonExec($(ev.currentTarget), this._editTeam);
//            this._buttonExec($(ev.currentTarget), this._editOpportunity);
        }
    },
//    _onCalendarIconClick: function (ev) {
//        $(ev.currentTarget).closest('div.date').datetimepicker({
//            format : time.getLangDateFormat(),
//            icons: {
//                time: 'fa fa-clock-o',
//                date: 'fa fa-calendar',
//                up: 'fa fa-chevron-up',
//                down: 'fa fa-chevron-down',
//            },
//        });
//    },

    _parse_date: function (value) {
        console.log(value);
        var date = moment(value, "YYYY-MM-DD", true);
        if (date.isValid()) {
            return time.date_to_str(date.toDate());
        }
        else {
            return false;
        }
    },
});
});
