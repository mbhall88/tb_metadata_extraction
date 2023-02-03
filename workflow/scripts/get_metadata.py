import sys

sys.stderr = open(snakemake.log[0], "w")
import requests
from requests import HTTPError
import xmltodict


def eprint(msg: str):
    print(msg, file=sys.stderr)


def main():
    biosample = snakemake.wildcards.biosample
    url_stem = snakemake.params.url_stem
    url = f"{url_stem}/{biosample}"
    eprint(f"Retrieving metadata for {biosample} from URL {url} ...")
    response = requests.get(url, timeout=snakemake.params.timeout)
    if response.status_code != 200:
        raise HTTPError(
            f"Got status code {response.status_code} with reason {response.reason}\n{response.text}"
        )

    xml = response.text
    xml_as_dict = xmltodict.parse(xml)
    attributes: list[dict[str, str]] = (
        xml_as_dict.get("SAMPLE_SET", {})
        .get("SAMPLE", {})
        .get("SAMPLE_ATTRIBUTES", {})
        .get("SAMPLE_ATTRIBUTE", {})
    )

    header = ["bioproject", "biosample"]
    row = [snakemake.wildcards.project, snakemake.wildcards.biosample]

    for attribute in attributes:
        tag = attribute["TAG"]
        value = attribute["VALUE"]
        header.append(tag)
        row.append(value)

    with open(snakemake.output.metadata, "w") as fp:
        print("\t".join(header), file=fp)
        print("\t".join(row), file=fp)


main()
