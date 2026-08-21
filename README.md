# LavinMQ RPM Packaging for Fedora & CentOS Stream

RPM packaging specifications, systemd dual service integration, and automated
Copr build workflows for [LavinMQ](https://github.com/cloudamqp/lavinmq).

LavinMQ is an open-source, high-performance message queue broker written in
Crystal, implementing the AMQP 0-9-1 protocol. Developed by CloudAMQP, it is
designed for ultra-low latency, high throughput, and minimal memory usage,
making it a lightweight alternative to heavier message brokers.

## Highlights & Features

* **High Throughput & Low Latency**: Processes up to 1,000,000+ messages per
  second with sub-millisecond latencies.
* **Minimal Memory Overhead**: Operates on tens of megabytes of RAM rather than
  gigabytes, streaming disk-backed message logs directly without GC stalls.
* **AMQP 0-9-1 Compatibility**: Drop-in protocol replacement for applications
  built for RabbitMQ.
* **Built-in Management UI & HTTP API**: Embedded web management dashboard
  supporting real-time queues, exchanges, connections, and Prometheus metrics.
* **Dual Service Units**: Pre-configured systemd units for both system-wide
  daemons and rootless user-session services.
* **Automated Packaging**: Maintained with continuous Copr builds and Packit
  upstream release tracking.

## Comparison

| Feature | LavinMQ | RabbitMQ | ActiveMQ |
| :--- | :--- | :--- | :--- |
| Runtime | Crystal | Erlang (BEAM) | Java (JVM) |
| Memory | ~20–50 MB | 200–500+ MB | 300–800+ MB |
| Protocol | AMQP 0-9-1 | AMQP, STOMP | AMQP, JMS |
| Storage | Disk mfile | Mnesia / Khepri | KahaDB |
| Standalone | Single binary | Erlang runtime | JVM runtime |

## Target Distributions

The Copr repository provides automated builds for:

* **Fedora Rawhide** (`x86_64`, `aarch64`)
* **Fedora 45** (`x86_64`, `aarch64`)
* **Fedora 44** (`x86_64`, `aarch64`)
* **Fedora 43** (`x86_64`, `aarch64`)
* **CentOS Stream 10** (`x86_64`, `aarch64`)
* **EPEL 10** (`x86_64`, `aarch64`)

## Installation

Enable the Copr repository and install the package using DNF:

```bash
sudo dnf copr enable renich/lavinmq
sudo dnf install lavinmq
```

## Quick Start & Service Management

### 1. System-Wide Service (Default)

To run LavinMQ as a dedicated system service under the `lavinmq` system user:

```bash
sudo systemctl enable --now lavinmq
```

Check service status and logs:

```bash
systemctl status lavinmq
sudo journalctl -u lavinmq -f
```

### 2. Rootless User-Session Service

For developer environments or unprivileged execution:

```bash
systemctl --user enable --now lavinmq
```

Check user service status:

```bash
systemctl --user status lavinmq
journalctl --user -u lavinmq -f
```

### 3. Management Web Interface

Once started, the management web dashboard is available at:

* URL: `http://127.0.0.1:15672`
* Default Credentials: `guest` / `guest`

## Command-Line Tools

### Server Management (`lavinmqctl`)

Inspect cluster and queue state:

```bash
lavinmqctl list_queues
lavinmqctl list_connections
lavinmqctl list_exchanges
```

### Performance Benchmarking (`lavinmqperf`)

Run high-load AMQP throughput benchmarks:

```bash
lavinmqperf --producers 4 --consumers 4 --rate 50000
```

## Configuration

* Configuration File: `/etc/lavinmq/lavinmq.ini`
* Data Directory (System): `/var/lib/lavinmq`
* Sysusers Definition: `/usr/lib/sysusers.d/lavinmq.conf`
* System Unit: `/usr/lib/systemd/system/lavinmq.service`
* User Unit: `/usr/lib/systemd/user/lavinmq.service`

## License

This packaging repository and upstream LavinMQ are licensed under the
[Apache-2.0 License](LICENSE).
