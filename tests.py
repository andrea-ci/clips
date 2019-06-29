#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest
import clips

class TestClips(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_simple_arg(self):

        console = clips.ArgParser('test')
        console.add_argument('arg')

        # no arg
        self.assertRaises(clips.ClipsError,console.parse_args,[])

        # arg
        args = console.parse_args(['arg'])
        self.assertEqual(args['arg'],'arg')
        self.assertFalse(args['--help'])
        self.assertFalse(args['-h'])


    def test_simple_opt(self):

        console = clips.ArgParser('test')
        console.add_argument('-o','--opt')
        console.add_argument('-a',)

        # no opt
        args = console.parse_args([])
        self.assertFalse(args['-o'])
        self.assertFalse(args['--opt'])
        self.assertFalse(args['-a'])

        # shorts
        args = console.parse_args(['-a'])
        self.assertFalse(args['-o'])
        self.assertFalse(args['--opt'])

        args = console.parse_args(['-o'])
        self.assertTrue(args['-o'])
        self.assertFalse(args['--opt'])

        # long
        args = console.parse_args(['--opt'])
        self.assertFalse(args['-o'])
        self.assertTrue(args['--opt'])

        # valued
        console = clips.ArgParser('test')
        console.add_argument('-a','--alpha',valued=True)
        args = console.parse_args([])
        self.assertFalse(args['-a'])
        args = console.parse_args(['-a10'])
        self.assertEqual(args['-a'],'10')
        args = console.parse_args(['--alpha=10'])
        self.assertEqual(args['--alpha'],'10')


    def test_simple_mixed_args(self):

        console = clips.ArgParser('test')
        console.add_argument('arg')
        console.add_argument('-o')

        self.assertRaises(clips.ClipsError,console.parse_args,[])

        args = console.parse_args(['arg'])
        self.assertTrue(args['arg'])
        self.assertFalse(args['-o'])

        args = console.parse_args(['arg','-o'])
        self.assertTrue(args['arg'])
        self.assertTrue(args['-o'])

        args = console.parse_args(['-o','arg'])
        self.assertTrue(args['arg'])
        self.assertTrue(args['-o'])

    def test_simple_command(self):

        console = clips.ArgParser('test')
        console.add_argument('arg1')
        console.add_argument('-a','--alpha')

        cmd = console.add_command('cmd')
        cmd.add_argument('arg2')
        cmd.add_argument('-a','--alpha')

        args = console.parse_args(['arg'])
        self.assertEqual(args['arg1'],'arg')
        self.assertFalse(args['cmd'])
        self.assertFalse(args['-a'])
        self.assertFalse(args['--alpha'])

        self.assertRaises(clips.ClipsError,console.parse_args,[])

        args = console.parse_args(['cmd','arg'])
        self.assertTrue(args['cmd'])
        self.assertEqual(args['arg2'],'arg')

        args = console.parse_args(['cmd','arg','-a'])
        self.assertEqual(args['arg2'],'arg')
        self.assertTrue(args['cmd'])
        self.assertTrue(args['-a'])

    def test_nested_command(self):

        console = clips.ArgParser('test')
        cmd1 = console.add_command('cmd1')
        cmd2 = cmd1.add_command('cmd2')

        cmd2.add_argument('arg2')
        cmd2.add_argument('-a','--alpha')

        args = console.parse_args(['cmd1'])
        self.assertTrue(args['cmd1'])
        self.assertFalse(args['cmd2'])

        self.assertRaises(clips.ClipsError,console.parse_args,['cmd1','cmd2'])
        self.assertRaises(clips.ClipsError,console.parse_args,['cmd2'])

        args = console.parse_args(['cmd1','cmd2','arg'])
        self.assertTrue(args['cmd1'])
        self.assertTrue(args['cmd2'])
        self.assertEqual(args['arg2'],'arg')


if __name__ == '__main__':
    unittest.main()
