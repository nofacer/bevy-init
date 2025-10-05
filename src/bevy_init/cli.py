import os
import subprocess
from pathlib import Path
import textwrap
import typer

app = typer.Typer(help="🚀 Quickly scaffold a new Bevy game project")


@app.command()
def new(
    project_name: str = typer.Argument(..., help="Name of the new Bevy project"),
    run: bool = typer.Option(
        False, "--run", "-r", help="Run cargo after creating the project"
    ),
):
    """
    Create a new Bevy project with a standard directory structure and optimized Cargo.toml.
    """

    project_dir = Path(project_name).resolve()

    typer.echo(f"🦀 Creating new Bevy project: {project_name}")
    subprocess.run(["cargo", "new", project_name], check=True)
    os.chdir(project_dir)

    typer.echo("➕ Adding Bevy dependency")
    subprocess.run(["cargo", "add", "bevy"], check=True)

    typer.echo("📁 Creating asset and source directories...")
    assets_dirs = [
        "images",
        "sounds",
        "models",
        "shaders",
        "fonts",
        "levels",
        "configs",
        "atlases",
        "animations",
        "materials",
    ]
    for d in assets_dirs:
        (project_dir / "assets" / d).mkdir(parents=True, exist_ok=True)

    for sub in ["systems", "components", "resources", "states", "utils"]:
        (project_dir / "src" / sub).mkdir(parents=True, exist_ok=True)

    typer.echo("🧾 Writing main.rs ...")
    main_rs = project_dir / "src" / "main.rs"
    main_rs.write_text(
        textwrap.dedent(
            """\
            use bevy::prelude::*;

            fn main() {
                App::new()
                    .add_plugins(DefaultPlugins)
                    .run();
            }
            """
        )
    )

    typer.secho(
        f"\n✅ Project '{project_name}' created successfully!", fg=typer.colors.GREEN
    )
    typer.echo("➡️  Next steps:")
    typer.echo(f"   cd {project_name}")
    typer.echo("   cargo run")

    if run:
        typer.echo("\n🚀 Running project...")
        subprocess.run(["cargo", "run"], check=True)


if __name__ == "__main__":
    app()
