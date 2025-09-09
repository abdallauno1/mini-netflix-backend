data "aws_ami" "amzn2" {
  most_recent = true
  owners      = ["137112412989"]
  filter { name = "name" values = ["amzn2-ami-hvm-*-x86_64-gp2"] }
}
resource "aws_key_pair" "this" { key_name = "${var.project_name}-key" public_key = file(var.public_key_path) }
resource "aws_security_group" "web_sg" {
  name = "${var.project_name}-sg" description = "Allow SSH and HTTP"
  ingress { from_port=22 to_port=22 protocol="tcp" cidr_blocks=["0.0.0.0/0"] }
  ingress { from_port=80 to_port=80 protocol="tcp" cidr_blocks=["0.0.0.0/0"] }
  egress  { from_port=0 to_port=0 protocol="-1" cidr_blocks=["0.0.0.0/0"] }
}
resource "aws_instance" "web" {
  ami = data.aws_ami.amzn2.id
  instance_type = var.instance_type
  key_name = aws_key_pair.this.key_name
  vpc_security_group_ids = [aws_security_group.web_sg.id]
  associate_public_ip_address = true
  tags = { Name = "${var.project_name}-web" }
}
