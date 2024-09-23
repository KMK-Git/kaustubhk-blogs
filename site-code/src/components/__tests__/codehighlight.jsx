import React from 'react';
import renderer from 'react-test-renderer';
import { themes } from 'prism-react-renderer';
import CodeHighlight from '../codehighlight';

describe('CodeHighlight', () => {
  it('renders correctly', async () => {
    const exampleCode = `cdk_codepipeline = pipelines.CodePipeline(
        self,
        "Pipeline",
        synth=pipelines.ShellStep(
            "Synth",
            input=source,
            install_commands=[
                "pip install -r requirements.txt",
                "npm install -g aws-cdk",
            ],
            commands=[
                "cdk synth",
            ],
        ),
    )`;
    const tree = renderer
      .create(<CodeHighlight theme={themes.vsDark} code={exampleCode} language="python" />)
      .toJSON();
    expect(tree).toMatchSnapshot();
  });
});
