import os
import argparse
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

# Initialize
load_dotenv()
client = OpenAI()


def start_batch_job(file_path):
    """Uploads a file and starts a new batch job."""
    print(f"Uploading batch file: {file_path}...")
    with open(file_path, "rb") as f:
        file_response = client.files.create(file=f, purpose="batch")

    print(f"Creating batch job for file: {file_response.id}")
    batch_job = client.batches.create(
        input_file_id=file_response.id,
        endpoint="/v1/chat/completions",
        completion_window="24h"
    )

    print("-" * 30)
    print(f"Batch Job Created Successfully!")
    print(f"Batch Job ID: {batch_job.id}")
    print(f"Status:       {batch_job.status}")
    print("-" * 30)
    print(f"Keep this ID to check progress later.")


def check_batch_status(batch_id):
    """Retrieves and prints the current status of a batch job with a progress bar."""
    job = client.batches.retrieve(batch_id)

    print("-" * 30)
    print(f"Batch ID: {job.id}")
    print(f"Status:   {job.status.upper()}")

    if job.request_counts:
        counts = job.request_counts
        total = counts.total
        completed = counts.completed
        failed = counts.failed
        processed = completed + failed

        # Initialize tqdm with the total count
        # bar_format gives you control over the layout
        with tqdm(total=total, desc="Progress", unit="req",
                  bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{percentage:3.0f}%]") as pbar:
            pbar.update(processed)

        print(f"Details: {completed} succeeded, {failed} failed")

    if job.status == "completed":
        print(f"\n✅ Ready for download! Output File ID: {job.output_file_id}")
    elif job.status == "failed":
        print(f"\n❌ Errors: {job.errors}")
    print("-" * 30)


def download_batch_results(batch_id, output_path):
    """Checks if a job is done and downloads the result to a local file."""
    job = client.batches.retrieve(batch_id)

    if job.status != "completed":
        print(f"Cannot download yet. Current status: {job.status}")
        return

    print(f"Downloading results from file {job.output_file_id}...")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Retrieve the content
    file_content = client.files.content(job.output_file_id)

    with open(output_path, "w") as f:
        f.write(file_content.text)

    print(f"✅ Success! Results saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="OpenAI Batch API Manager")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Command: start
    start_parser = subparsers.add_parser("start", help="Upload file and start a new job")
    start_parser.add_argument("--file", default="data/batch_input.jsonl", help="Path to input JSONL file")

    # Command: check
    check_parser = subparsers.add_parser("check", help="Check status of an existing job")
    check_parser.add_argument("id", help="The Batch Job ID")

    # Command: download
    download_parser = subparsers.add_parser("download", help="Download results of a completed job")
    download_parser.add_argument("id", help="The Batch Job ID")
    download_parser.add_argument("--output", default="data/batch_output.jsonl", help="Where to save the results")

    args = parser.parse_args()

    if args.command == "start":
        start_batch_job(args.file)
    elif args.command == "check":
        check_batch_status(args.id)
    elif args.command == "download":
        download_batch_results(args.id, args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()