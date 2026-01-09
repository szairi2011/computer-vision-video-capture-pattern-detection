"""Main entry point with Click CLI for PoC demo."""

import click
from pathlib import Path

from .pipeline.orchestrator import process_shelf_video, PipelineConfig
from .config.settings import get_settings


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Fruits Quality Detection System - Supermarket shelf monitoring PoC."""
    pass


@cli.command()
@click.option('--source', '-s', required=True, help='Video source (camera index, file, or URL)')
@click.option('--output', '-o', help='Output video file path')
@click.option('--max-frames', '-m', default=0, help='Max frames to process (0 = unlimited)')
@click.option('--conf', '-c', default=0.3, help='Detection confidence threshold')
@click.option('--events/--no-events', default=False, help='Enable Event Hub publishing')
@click.option('--search/--no-search', default=False, help='Enable AI Search indexing')
@click.option('--display/--no-display', default=True, help='Display video window')
def detect(source, output, max_frames, conf, events, search, display):
    """Run fruit quality detection on video source."""
    config = PipelineConfig(
        source=source,
        output_path=output,
        max_frames=max_frames,
        detector_conf=conf,
        enable_events=events,
        enable_search=search,
        display=display
    )
    
    click.echo(f"Processing video from: {source}")
    stats = process_shelf_video(config)
    
    click.echo("\n=== Processing Complete ===")
    click.echo(f"Frames processed: {stats['frames_processed']}")
    click.echo(f"Detections: {stats['detections']}")
    click.echo(f"Events published: {stats['events_published']}")
    click.echo(f"Documents indexed: {stats['documents_indexed']}")


@cli.command()
def demo():
    """Run quick demo with webcam (no Azure integration)."""
    click.echo("Starting demo mode with webcam...")
    
    config = PipelineConfig(
        source="0",
        max_frames=300,  # ~10 seconds at 30fps
        detector_conf=0.3,
        enable_events=False,
        enable_search=False,
        display=True
    )
    
    stats = process_shelf_video(config)
    click.echo(f"\nDemo complete: {stats['frames_processed']} frames, {stats['detections']} detections")


@cli.command()
def config():
    """Show current configuration."""
    settings = get_settings()
    
    click.echo("\n=== Current Configuration ===")
    click.echo(f"YOLO Model: {settings.yolo_model}")
    click.echo(f"Detection Confidence: {settings.detection_confidence}")
    click.echo(f"Output Directory: {settings.output_directory}")
    click.echo(f"\nAzure Event Hub: {'Configured' if settings.event_hub_connection_string else 'Not configured'}")
    click.echo(f"Azure AI Search: {'Configured' if settings.search_endpoint else 'Not configured'}")


if __name__ == "__main__":
    cli()
