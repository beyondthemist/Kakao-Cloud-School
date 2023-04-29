resource "aws_instance" "ubuntu_bastion" {
  ami = "ami-0e38c97339cddf4bd"
  availability_zone = "ap-northeast-2a"
  instance_type = "t2.micro"
  key_name = "kirisame"
  vpc_security_group_ids = [aws_security_group.bastion_sg.id]
  subnet_id = module.vpc.public_subnets[0]
  associate_public_ip_address = true

  connection {
    type = "ssh"
    user = "ubuntu"
    private_key = file("../kirisame.pem")
    host = self.public_ip
  }
  
  provisioner "file" {
    source      = "./install.sh"
    destination = "~/install.sh"
  }
  /*  
  provisioner "remote-exec" {
    inline = [
      "sudo sh ../ubuntu/install.sh"
    ]
  }
  */
  tags = {
      Name = "ubuntu_bastion"
  }
}
