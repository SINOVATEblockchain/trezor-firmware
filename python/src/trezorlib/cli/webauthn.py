# This file is part of the Trezor project.
#
# Copyright (C) 2012-2019 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import click

from .. import webauthn


@click.group(name="webauthn")
def cli():
    """WebAuthn management commands."""


@cli.command()
@click.pass_obj
def list_credentials(connect):
    """List all resident credentials on the device."""
    creds = webauthn.list_credentials(connect())
    for cred in creds:
        click.echo("")
        click.echo("WebAuthn credential at index {}:".format(cred.index))
        if cred.rp_id is not None:
            click.echo("  Relying party ID:       {}".format(cred.rp_id))
        if cred.rp_name is not None:
            click.echo("  Relying party name:     {}".format(cred.rp_name))
        if cred.user_id is not None:
            click.echo("  User ID:                {}".format(cred.user_id.hex()))
        if cred.user_name is not None:
            click.echo("  User name:              {}".format(cred.user_name))
        if cred.user_display_name is not None:
            click.echo("  User display name:      {}".format(cred.user_display_name))
        if cred.creation_time is not None:
            click.echo("  Creation time:          {}".format(cred.creation_time))
        if cred.hmac_secret is not None:
            click.echo("  hmac-secret enabled:    {}".format(cred.hmac_secret))
        if cred.use_sign_count is not None:
            click.echo("  Use signature counter:  {}".format(cred.use_sign_count))
        click.echo("  Credential ID:          {}".format(cred.id.hex()))

    if not creds:
        click.echo("There are no resident credentials stored on the device.")


@cli.command()
@click.argument("hex_credential_id")
@click.pass_obj
def add_credential(connect, hex_credential_id):
    """Add the credential with the given ID as a resident credential.

    HEX_CREDENTIAL_ID is the credential ID as a hexadecimal string.
    """
    return webauthn.add_credential(connect(), bytes.fromhex(hex_credential_id))


@cli.command()
@click.option(
    "-i", "--index", required=True, type=click.IntRange(0, 15), help="Credential index."
)
@click.pass_obj
def webauthn_remove_credential(connect, index):
    """Remove the resident credential at the given index."""
    return webauthn.remove_credential(connect(), index)