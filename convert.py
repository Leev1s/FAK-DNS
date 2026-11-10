import os
from pathlib import Path


def convert_conf_to_txt(conf_file, txt_file, cn_dns):
    with conf_file.open(encoding='utf-8') as conf, txt_file.open('w', encoding='utf-8') as txt:
        for number, line in enumerate(conf, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if not line.startswith('server=/') or line.count('/') < 2:
                raise ValueError(f'{conf_file}:{number}: invalid dnsmasq rule: {line}')
            domain = line.split('/', 2)[1]
            if not domain:
                raise ValueError(f'{conf_file}:{number}: empty domain')
            txt.write(f'[/{domain}/]{cn_dns}\n')


def main():
    cn_upstreams = os.environ.get('CN_DNS', '').split()
    default_upstreams = [line.strip() for line in os.environ.get('THE_DNS', '').splitlines()
                         if line.strip()]
    if not cn_upstreams or not default_upstreams:
        raise ValueError('CN_DNS and THE_DNS must both be set')
    if any(len(line.split()) != 1 for line in default_upstreams):
        raise ValueError('THE_DNS must contain one DNS server per line')
    cn_dns = ' '.join(cn_upstreams)

    root = Path.cwd()
    converted = root / 'converted'
    converted.mkdir(exist_ok=True)
    conf_files = sorted(p for p in root.glob('*china.conf')
                        if p.name != 'bogus-nxdomain.china.conf')
    if not conf_files:
        raise ValueError('No domain list files found')
    output_files = []
    for conf_file in conf_files:
        txt_file = converted / f'{conf_file.name}.txt'
        convert_conf_to_txt(conf_file, txt_file, cn_dns)
        output_files.append(txt_file)

    with (converted / 'FAK-DNS.txt').open('w', encoding='utf-8') as combined:
        combined.write('\n'.join(default_upstreams) + '\n')
        for txt_file in output_files:
            combined.write(txt_file.read_text(encoding='utf-8'))


if __name__ == '__main__':
    main()
