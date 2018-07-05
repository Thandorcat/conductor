import contextlib
import os
import re
import subprocess
import sys


class Provider:

    def __init__(self):

        self.root = os.path.abspath(root) if root is not None else os.getcwd()
        self._cached_conf = {}
        self._vagrant_exe = None
        self.env = env
        self.type = 'vagrant'

    def handle_exception(fn):
        def wrapped(self, *args):
            try:
                return fn(self, *args)
            except Exception as e:
                self.message += str(e)
                return self.message, 500

        return wrapped

    @handle_exception
    def run(self, options):

        provider_arg = '--provider=%s' % provider if provider else None
        prov_with_arg = None if provision_with is None else '--provision-with'
        providers_arg = None if provision_with is None else ','.join(provision_with)

        if provision is not None:
            no_provision = None
        no_provision_arg = '--no-provision' if no_provision else None
        provision_arg = None if provision is None else '--provision' if provision else '--no-provision'

        args = ['up', vm_name, no_provision_arg, provision_arg, provider_arg, prov_with_arg, providers_arg]
        if stream_output:
            generator = self._stream_vagrant_command(args)
        else:
            self._call_vagrant_command(args)

        self._cached_conf[vm_name] = None
        return generator if stream_output else None

    @handle_exception
    def restart(self, vm_name):

        prov_with_arg = None if provision_with is None else '--provision-with'
        providers_arg = None if provision_with is None else ','.join(provision_with)
        provision_arg = None if provision is None else '--provision' if provision else '--no-provision'

        args = ['reload', vm_name, provision_arg, prov_with_arg, providers_arg]
        if stream_output:
            generator = self._stream_vagrant_command(args)
        else:
            self._call_vagrant_command(args)

        self._cached_conf[vm_name] = None
        return generator if stream_output else None

    @handle_exception
    def spot(self, vm_name):

        self._call_vagrant_command(['destroy', vm_name, '--force'])
        self._cached_conf[vm_name] = None

    @handle_exception
    def box_list(self):

        output = self._run_vagrant_command(['box', 'list', '--machine-readable'])
        return self._parse_box_list(output)